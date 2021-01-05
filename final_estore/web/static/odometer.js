const pad = function (n, width, z) {
    z = z || '0';
    n = n + '';
    return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

const setDigit = async function (type, digit) {
    const currentDigit = $(`.${type}`).text();
    if (currentDigit == digit) {
        return;
    }

    $(`.${type}`).addClass('digit-transform');
    await setTimeout(function () {
        $(`.${type}`).remove();
        $(`#${type}`).append(`<div class="digit-container ${type} digit-slide">${digit}</div>`);
        setTimeout(function () {
            $(`.${type}`).removeClass("digit-slide");
        }, 1000)
    }, 300);
}

const addCount = async function (count) {
    if (count >= 999) {
        return;
    }
    const newCount = count + 1;
    const newCountArray = getCountArray(newCount);
    await setDigit('digit-hundred', newCountArray[0]);
    await setDigit('digit-ten', newCountArray[1]);
    await setDigit('digit-one', newCountArray[2]);
    return newCount;
}

const removeCount = async function (count) {
    if (count <= 0) {
        return;
    }
    const newCount = count - 1;
    const newCountArray = getCountArray(newCount);
    $(".digit-one").addClass('digit-transform');
    await setDigit('digit-hundred', newCountArray[0]);
    await setDigit('digit-ten', newCountArray[1]);
    await setDigit('digit-one', newCountArray[2]);
    return newCount;
}

const getCountArray = function (count) {
    let countString = pad(count, 3);
    return [countString.charAt(0), countString.charAt(1), countString.charAt(2)];
}

const setCount = function (count) {
    let countArray = getCountArray(count);

    $(".digit-hundred").text(countArray[0]);
    $(".digit-ten").text(countArray[1]);
    $(".digit-one").text(countArray[2]);
}

const getOdometerHtml = function () {
    return ` <div class="odometer-wrapper mb-3">
                <div class="odometer-face">
                    <div class="digit" id="digit-hundred">
                        <div class="digit-container digit-hundred">0</div>
                    </div>
                    <div class="digit" id="digit-ten">
                        <div class="digit-container digit-ten">0</div>
                    </div>
                    <div class="digit" id="digit-one">
                        <div class="digit-container digit-one">0</div>
                    </div>
                </div>
            </div>`;
}