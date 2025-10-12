// 自定义 JSEncrypt
const JSEncrypt = require('./jsencrypt')
const CryptoJS = require('crypto-js')

function u(e) {
    var n = new JSEncrypt;
    return n.setPublicKey("-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC1vKwZUIv7pgpJUXXPpDlD4+VE\non3a0ANOrNmqAESrcGfkmYzDCo2JeuYezhBGjBNjwVmSct/Y3BBOCRGT2bvtCJGd\nS12RMvHbFcdbwS/Adh48+rhLiMNYXLm+7pI3e2k6TlScxKa7EeeZpVtew/Cv5z6o\nl0llNPp6BdqAlOa8DwIDAQAB\n-----END PUBLIC KEY-----"), n.encrypt(e) || ""
}

function encrypt(page) {
    var c = parseInt(page),
        a = "fsymmetry_challenge",
        o = Date.now(),
        s = "".concat(c, "_").concat(a, "_").concat(o);
    key = u(s),
        signature = (
            n = s,
                t = new JSEncrypt(),
                t.setPrivateKey("-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQC1vKwZUIv7pgpJUXXPpDlD4+VEon3a0ANOrNmqAESrcGfkmYzD\nCo2JeuYezhBGjBNjwVmSct/Y3BBOCRGT2bvtCJGdS12RMvHbFcdbwS/Adh48+rhL\niMNYXLm+7pI3e2k6TlScxKa7EeeZpVtew/Cv5z6ol0llNPp6BdqAlOa8DwIDAQAB\nAoGAS0GaWI9AsFAFEXBgoz/jkMf14DKTgEFEJVexeNLMnNuawhCNuBSOIMCaO2Zk\nWfpWaygdUeYs6M3UGKRruXhf92g/BRmJK5FzR0kWW4qw6WwlYob3TPc3c9MFOjmp\nVtWQ0VSeEPrnBNoQRccKl0dGBnToHGuV+KEuKx8oWZc/JM0CQQDH/cvlx0BKz2zN\n6PM8FidAvc+Wgon8YW81KJgC7iJIrK9FOpctOE3L1pdF7guOQNVGRqN4HCIgLfHE\ncqxWJKJtAkEA6KIkwHe/Q23uWH5GP8DHtVkLVfohTumYkpb0rk05EYQ0dsWSNzWH\nXDH/kD6ayNq+fscnS8g+59onzvfhJ0bq6wJBAKNFkDEHenWY4js481sauvEgBVnb\nOMvSv/emLHQ39cVfNbhPHRzN2rWPe/CbZtO8GmJFSS/FyBZ9a+P1uryZLAECQAaw\nApZ12s25b0yj9KkIhbU05hqGokZ+eKBeLpKELcvPHSL88wMbStTfqxUed5ymjStf\n1kVbcFOB9fsBLTvP0hkCQFCON0l1VjFli+vqfN0lypgIqCf85V6FZFN19creGCCd\n76pX/X2FIBbUSDN1z48SM5I/RKdCkTx7FY+509q2Mek=\n-----END RSA PRIVATE KEY-----"),
            t.sign(n, CryptoJS.SHA256, "sha256") || ""
        )
    ;
    var i = function (e) {
            return CryptoJS.HmacSHA256(e, "dsa_secret_key_2025").toString()
        }(s),
        l = u(s + "_param")
    return {data: l, verify: i, t: o, key, signature}
}

console.log(encrypt(1));