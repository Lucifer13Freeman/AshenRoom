
// Menu

const dropdown_menu = document.querySelector('.dropdown_menu');
const dropdown_button = document.querySelector('.dropdown_button');

if (dropdown_button) dropdown_button.addEventListener('click', () => 
{
  dropdown_menu.classList.toggle('show');
});

// Upload Image
const photo_input = document.querySelector('#avatar');
const photo_preview = document.querySelector('#preview_avatar');

if (photo_input) photo_input.onchange = () => 
{
  const [file] = photo_input.files;
  if (file) photo_preview.src = URL.createObjectURL(file);
};

// Scroll to Bottom
const room_chat_thread = document.querySelector('.room_box');
if (room_chat_thread) room_chat_thread.scrollTop = room_chat_thread.scrollHeight;
