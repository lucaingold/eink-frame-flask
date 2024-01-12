const posts = [];
const images = [
  '1.bmp',
  '2.bmp',
  '4.bmp',
  '5.bmp',
  '6.bmp',
  '7.bmp',
  '8.bmp',
  '9.bmp',
  '10.bmp',
  '11.bmp',
  '12.bmp',
  '13.bmp',
  '14.bmp',
  '15.bmp',
  '16.bmp',
  '17.bmp',
  '18.bmp',
  '19.bmp',
  '20.bmp',
  '21.bmp',
  '22.bmp',
  '23.bmp',
  '24.bmp',
  '25.bmp',
  '26.bmp',
  '27.bmp',
  '28.bmp',
  '29.bmp',
  '30.bmp',
  '31.bmp',
];

let imageIndex = 0;

for (let i = 1; i <= 30; i++) {
  let item = {
    id: i,
    title: `Click to send to Ink-Frame`,
    image: `static/pictures/` + images[imageIndex].replace('.bmp', '.jpeg'),
    path: `path=./pic/new/` + images[imageIndex],

  };
  posts.push(item);
  imageIndex++;
  if (imageIndex > images.length - 1) imageIndex = 0;
}
