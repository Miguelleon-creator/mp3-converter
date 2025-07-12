document.getElementById('button-converter').addEventListener('click', async () => {

    const urlvideo = document.getElementById('urlvideo').value.trim();

    const menssageScript = document.getElementById('menssageScript');

    if(!urlvideo) {
        menssageScript.textContent = "Please, put a valid URL.";
        return;
    }

    menssageScript.textContent = "Converting... please wait a few seconds.";

    try {
        const correct = await fetch(`/convert?url=${encodeURIComponent(urlvideo)}`);

        if (!correct.ok) {
            menssageScript.textContent = "An error occurred. Please try again.";
            return;
        }

        const blob = await correct.blob();
        
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement('a');

        a.href = url;

        a.download = "video.mp3";

        document.body.appendChild(a);
        
        a.click();

        a.remove();

        menssageScript.textContent = "Download Ready!";
    } catch (error) {
        console.error(error);
        menssageScript.textContent = "An error occurred. Try again later.";
    }
});