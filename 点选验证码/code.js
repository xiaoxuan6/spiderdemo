function encrypt(e) {
    const _0x2ea633 = JSON['stringify'](e);
    return btoa(unescape(encodeURIComponent(_0x2ea633)));
}

let data = [
    [
        255,
        235
    ],
    [
        162,
        81
    ],
    [
        35,
        216
    ],
    [
        354,
        246
    ]
]
console.log(encrypt(data));