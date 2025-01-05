let time = document.getElementById("time");

let addLeadingZero = (value) => {
    if (value < 10) {
        return "0" + String(value);
    }
    return value;
};

let setCurrentTime = () => {
    let date = new Date();
    let timeString = `${addLeadingZero(date.getDate())}.${addLeadingZero(date.getMonth() + 1)}.${date.getFullYear()} ${addLeadingZero(date.getHours())}:${addLeadingZero(date.getMinutes())}:${addLeadingZero(date.getSeconds())}`
    time.innerText = timeString;

};

setCurrentTime()
setInterval(setCurrentTime, 1000);