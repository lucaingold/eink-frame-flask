# Set the local directory

GIT_REPO=https://github.com/lucaingold/eink-frame-flask

LOCAL_DIR="$HOME/$(basename $GIT_REPO)"
IMAGES_DIR="${LOCAL_DIR}/$(basename $GIT_REPO)/static/pictures/"

# File paths
SERVICE_DIR=/etc/systemd/system
SERVICE_FILE=einkframe.service
SERVICE_FILE_TEMPLATE=einkframe.service.template


function install_linux_packages(){
  sudo apt-get update
  sudo apt-get install -y git python3-pip libatlas-base-dev pass gnupg2 jq libopenjp2-7
}


#function install_pijuice_package(){
#  # Install pijuice.
#  sudo apt-get install -y pijuice-base pijuice-gui
#  echo -e "PiJuice installed"
#}


#function install_python_packages(){
#}


#function disable_leds(){
#  cd "${LOCAL_DIR}" || exit
#  sudo python3 "${LOCAL_DIR}/${LED_SCRIPT}"
#  echo -e "PiJuice LEDS disabled"
#}

function setup_hardware(){
  echo "Setting up SPI"
  if ls /dev/spi* &> /dev/null; then
      echo -e "SPI already enabled"
  else
      if command -v raspi-config > /dev/null && sudo raspi-config nonint get_spi | grep -q "1"; then
          sudo raspi-config nonint do_spi 0
          echo -e "SPI is now enabled"
      else
          echo -e "${RED}There was an error enabling SPI, enable manually with sudo raspi-config${RESET}"
      fi
  fi
}

function service_installed(){
  # return 0 if the service is installed, 1 if no
  if [ -f "$SERVICE_DIR/$SERVICE_FILE" ]; then
    return 0
  else
    return 1
  fi
}

function copy_service_file(){
  sudo mv $SERVICE_FILE $SERVICE_DIR
  sudo systemctl daemon-reload
}

function install_service(){
  if [ -d "${LOCAL_DIR}" ]; then
    cd "$LOCAL_DIR" || return

    # generate the service file
    envsubst <$SERVICE_FILE_TEMPLATE > $SERVICE_FILE

    if ! (service_installed); then
      # install the service files and enable
      copy_service_file
      sudo systemctl enable einkframe

      echo -e "einkframe service installed! Use '${GREEN}sudo systemctl restart einkframe${RESET}' to test"
    else
      echo -e "${YELLOW}einkframe service is installed, checking if it needs an update${RESET}"
      if ! (cmp -s "einkframe.service" "/etc/systemd/system/einkframe.service"); then
        copy_service_file
        echo -e "Updating einkframe service file"
      else
        # remove the generated service file
        echo -e "No update needed"
        rm $SERVICE_FILE
      fi
    fi
  else
    echo -e "${RED}einkframe repo does not exist! Use option 1 - Install/Upgrade einkframe first${RESET}"
  fi

  # go back to home
  cd "$HOME" || return
}

function uninstall_service(){
  if (service_installed); then
    # stop if running and remove service files
    sudo systemctl stop einkframe
    sudo systemctl disable einkframe
    sudo rm "${SERVICE_DIR}/${SERVICE_FILE}"
    sudo systemctl daemon-reload

    echo -e "einkframe service was successfully uninstalled"
  else
    echo -e "${RED}einkframe service is already uninstalled.${RESET}"
  fi
}


function setup_smb(){
  sudo apt update
  sudo apt install samba -y

  echo "
    [images]
    comment = Images folder for einkframe
    path = ${IMAGES_DIR}
    public = yes
    writable = yes
    guest ok = yes
    security = SHARE
    " | sudo tee "${SMB_EINKFRAME_LOCATION}"

    sudo chmod -R 777 "${IMAGES_DIR}"

  if grep -Fq "${SMB_EINKFRAME_LOCATION}" ${SMB_DEFAULT_LOCATION}
  then
        echo "${YELLOW}'${SMB_EINKFRAME_LOCATION}' already exists in ${SMB_DEFAULT_LOCATION}${RESET}"
  else
        echo "Adding '${SMB_EINKFRAME_LOCATION}' to ${SMB_DEFAULT_LOCATION}"
        echo "include = ${SMB_EINKFRAME_LOCATION}" | sudo tee -a /etc/samba/smb.conf
  fi

  sudo systemctl enable smbd
  sudo systemctl restart smbd
  echo "SMB installed and folders '${PROMPTS_DIR}' and '${IMAGES_DIR}' shared with ${YELLOW}full permissions${RESET}"
}