#include <sodium.h>

// compile : g++ -o obj filename.c -lsodium

void PRG(char *buf, char *seed) {
    const size_t size=32;   
    randombytes_buf_deterministic(buf, size,seed);
}

void create_key_pair(char *pk, char *sk) {
    int r = crypto_sign_keypair(pk,sk);
    if(r==0)
    printf("key pair created\n");
    else
    printf("failed in keypair creation\n");
}

// crypto_sign_BYTES use for sig length

void get_sign(char *sig, char *msg, char * sk) {
    crypto_sign_detached(sig, NULL, msg, strlen(msg), sk);
}

//  It returns -1 if the signature fails verification, or 0 on success.

int verify(char *sig,char *msg, char * pk) {
    int retval = crypto_sign_verify_detached(sig, msg, strlen(msg), pk);
    return retval;
}

// -1 if b1_ is less than b2_
// 0 if b1_ equals b2_
// 1 if b1_ is greater than b2_

int compare(char *buf1,char *buf2) {
    const size_t size=32;
    int retval = sodium_compare(buf1, buf2, size);
    return retval;
}


