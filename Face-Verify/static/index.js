function deleteImg(imgId) {
    fetch('/delete-image', {
        method: 'POST',
        body: JSON.stringify({ imgId: imgId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}