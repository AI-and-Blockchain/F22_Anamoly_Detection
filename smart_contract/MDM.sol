// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;


contract MDM {

    uint128 con = 0.039311655805354055 * (10 ** 18);
    int128[4] mu;
    int128[4] sigma; 
    int128[4] mu2;
    int128[4][4] sig_inv;
    uint128 threshold = 0.004737994576574647 * (10 ** 18);

    constructor() {
        int128 a = 98;
        int128 b = 32;
        int128 c = -40;
        int128 d = 655;
        mu2 = [a, b, c, d];

        a = 5.502220741056456 * (10 ** 18);
        b = 104917.41897618743 * (10 ** 18);
        c = 12.274041973813828 * (10 ** 18);
        d = 8.860290641457999 * (10 ** 18);
        mu = [a, b, c, d];

        a = 7.054427631499825 * (10 ** 18);
        b = 391418.45899804303 * (10 ** 18);
        c = 4.846098041871643 * (10 ** 18);
        d = 6.946700908609921 * (10 ** 18);
        sigma = [a, b, c, d];

        int128 e = 2.05904074 * (10 ** 18);
        int128 f = -0.48093814 * (10 ** 18);
        int128 g = -0.75351254 * (10 ** 18);
        int128 h = 1.41395853 * (10 ** 18);
        sig_inv[0] = [e, f, g, h];
        sig_inv[1] = [-0.48093814 * (10 ** 18),  1.13400368 * (10 ** 18),  0.2042855 * (10 ** 18),  -0.19389946 * (10 ** 18)];
        sig_inv[2] = [-0.75351254 * (10 ** 18),  0.2042855 * (10 ** 18),   1.42148603 * (10 ** 18), -0.921056 * (10 ** 18)];
        e =  1.41395853 * (10 ** 18);
        f =  -0.19389946 * (10 ** 18);
        g = -0.921056 * (10 ** 18); 
        h = 2.13412928 * (10 ** 18);
        sig_inv[3] = [e, f, g, h];
    }

    function detection(int128 x0, int128 x1, int128 x2, int128 x3) public view returns (bool){

        int128 x0_s = (x0 - mu[0]) / sigma[0] - mu2[0];
        int128 x1_s = (x1 - mu[1]) / sigma[1] - mu2[1];
        int128 x2_s = (x2 - mu[2]) / sigma[2] - mu2[2];
        int128 x3_s = (x3 - mu[3]) / sigma[3] - mu2[3];

        int128 i0 = x0_s * sig_inv[0][0] + x1_s * sig_inv[0][1] + x2_s * sig_inv[0][2] + x3_s * sig_inv[0][3];
        int128 i1 = x0_s * sig_inv[1][0] + x1_s * sig_inv[1][1] + x2_s * sig_inv[1][2] + x3_s * sig_inv[1][3];
        int128 i2 = x0_s * sig_inv[2][0] + x1_s * sig_inv[2][1] + x2_s * sig_inv[2][2] + x3_s * sig_inv[2][3];
        int128 i3 = x0_s * sig_inv[3][0] + x1_s * sig_inv[3][1] + x2_s * sig_inv[3][2] + x3_s * sig_inv[3][3];

        uint128 exponent = uint128(i0 * x0_s + i1 * x1_s + i2 * x2_s + i3 * x3_s);
        uint128 e = (2.71828 * (10 ** 18));
        uint128 p = con * (e ** exponent);

        if(p <= threshold){
            return true;
        }
        return false;
        
    }
}