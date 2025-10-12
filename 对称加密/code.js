const CryptoJS = require('crypto-js')

function l(e) {
    var n = CryptoJS.enc.Utf8.parse("6f726c64")
        , t = CryptoJS.enc.Utf8.parse("01234567");
    return CryptoJS.DES.encrypt(e, n, {
        iv: t,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    }).toString()
}

function encrypt(page) {
    var a = parseInt(page)
        , c = "symmetry_challenge"
        , s = Date.now()
        , i = "".concat(a, "_").concat(c, "_").concat(s);
    var p = function (e) {
        var n = CryptoJS.enc.Utf8.parse("12345678901234567890123456789012"),
            t = CryptoJS.enc.Utf8.parse('abcdefghijklmnop');
        return CryptoJS.AES.encrypt(e, n, {
            iv: t,
            mode: CryptoJS.mode.OFB,
            padding: CryptoJS.pad.NoPadding
        }).toString()
    }(i), f = l(i + "_param")

    aes_token = (n = i,
        t = CryptoJS.enc.Utf8.parse("1234567890123456"),
        r = CryptoJS.enc.Utf8.parse('abcdefghijklmnop'),
        CryptoJS.AES.encrypt(n, t, {
            iv: r,
            mode: CryptoJS.mode.CTR,
            padding: CryptoJS.pad.NoPadding
        }).toString())
    des_token = l(i)

    return {p, f, s, aes_token, des_token}
}

console.log(encrypt(3));