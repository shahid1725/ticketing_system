const messages = document.querySelectorAll('.message');


  messages.forEach(message => {
    setTimeout(() => {
      message.remove();
    }, 2000);
  });