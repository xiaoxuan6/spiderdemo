const CryptoJS = require('crypto-js')
const sha3_256 = require('js-sha3').sha3_256

a = "hash_challenge";
const o = "spiderdemo_sha_salt_2025";

function r(e, t, n) {
    const s = `${e}_${t}_${n}`, a = (r = s, c = "spiderdemo_hmac_secret_2025", CryptoJS.HmacSHA256(r, c).toString());
    var r, c;
    const i = function (e) {
        return CryptoJS.MD5(e).toString()
    }(s + "spiderdemo_md5_salt_2025"), l = function (e) {
        return CryptoJS.SHA256(e).toString()
    }(s + o), u = function (e) {
        return sha3_256(e)
    }(s + o);
    return {
        hmac: a, md5: i, sha256: l, sha3_256: u
    }
}

function encrypt(page) {
    const n = parseInt(page), s = "hash_challenge", a = Date.now(), o = r(n, s, a);

    x_token = o.hmac
    x_code = o.md5
    sign = o.sha256
    code = o.sha3_256
    t = a

    return {x_token, x_code, sign, code, t}
}

console.log(encrypt(1));