const container = document.querySelector('.picture-container');

function generateMasonryGrid(columns, posts) {
  container.innerHTML = '';

  //Store column arrays that contain relevant posts
  let columnWrappers = {};

  //Create column item array and  add this to column wrapper object
  for (let i = 0; i < columns; i++) {
    columnWrappers[`column${i}`] = [];
  }
  for (let i = 0; i < posts.length; i++) {
    const column = i % columns;
    columnWrappers[`column${column}`].push(posts[i]);
  }
  for (let i = 0; i < columns; i++) {
    let columnPosts = columnWrappers[`column${i}`];
    let column = document.createElement('div');
    column.classList.add('column');
    columnPosts.forEach((posts) => {
      let postDiv = document.createElement('div');
      postDiv.classList.add('post');
      postDiv.setAttribute('onclick', `showImage('${posts.path}')`);
      let image = document.createElement('img');
      image.src = posts.image;
      let overlay = document.createElement('div');
      overlay.classList.add('overlay');
      let title = document.createElement('h3');
      title.innerText = posts.title;

      overlay.appendChild(title);
      postDiv.append(image, overlay);
      column.appendChild(postDiv);
    });
    container.appendChild(column);
  }
}

function showImage(path) {
  $('#spinner-container').show();

  // // Simulate an AJAX request delay (remove this in your actual code)
  // setTimeout(function() {
  //   // Simulated successful response
  //   console.log('Success');
  //
  //   // Hide the spinner when the request is complete
  //   $('#spinner-container').hide();
  // }, 4000);

  $.ajax({
    url: 'http://inkframe.local:8080',
    type: 'POST',
    contentType: 'text/plain',
    data: path,
    success: function(response) {
      console.log('Success:', response);
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.error('There was a problem with the fetch operation:', errorThrown);
      alert("Error! See console for more information.")
    },
    complete: function() {
      $('#spinner-container').hide();
    }
  });
}



let previousScreenSize = innerWidth;
console.log(previousScreenSize);

window.addEventListener('resize', () => {
  imageIndex = 0;
  if (innerWidth < 600 && previousScreenSize >= 600) {
    generateMasonryGrid(1, posts);
  } else if (
    innerWidth >= 600 &&
    innerWidth < 1000 &&
    (previousScreenSize < 600 || previousScreenSize >= 1000)
  ) {
    generateMasonryGrid(2, posts);
  } else if (innerWidth >= 1000 && previousScreenSize < 1000) {
    generateMasonryGrid(4, posts);
  }
  previousScreenSize = innerWidth;
});

//Page Load
if (previousScreenSize < 600) {
  generateMasonryGrid(1, posts);
} else if (previousScreenSize >= 600 && previousScreenSize < 1000) {
  generateMasonryGrid(2, posts);
} else {
  generateMasonryGrid(4, posts);
}
