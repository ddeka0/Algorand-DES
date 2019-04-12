#include <sodium.h>
#include <math.h>

int main(void) {
    if (sodium_init() < 0) {
        /* panic! the library couldn't be initialized, it is not safe to use */
    }
    char pk[32];
    char sk[32];
    char seed[256] = "HASHOFPREVIOUSBLOCK||ROUNDNUMBER||STEPNUMBER1";
    char seed2[256] = "HASHOFPREVEPNUMBER";
    // PRG(buffer,seed);
    // PRG(buffer2,seed2);
        int r = crypto_sign_keypair(pk,sk);
    // for(int i=0;i<32;i++)
    //     printf("%u",buffer[i]);
    // printf("\n");
    // for(int i=0;i<32;i++)
    //     printf("%u",buffer2[i]);
    // printf("\n");

    printf("return : %d\n",r);

    unsigned char sig[crypto_sign_BYTES];

    printf("%d\n",crypto_sign_BYTES);

    crypto_sign_detached(sig, NULL, "hello", strlen("hello"), sk);
    for(int i=0;i<crypto_sign_BYTES;i++)
        printf("%u",sig[i]);
    printf("\n");
   

    if (crypto_sign_verify_detached(sig, "hello", strlen("hello"), pk) != 0) {
    printf("incorrect\n");
    }
    return 0;
}

void PRG(char *buf, char *seed) {
	const size_t size=32;
	randombytes_buf_deterministic(buf, size,seed);
}

int compare(char *buf1,char *buf2) {
    const size_t size=32;
    int retval = sodium_compare(buf1, buf2, size);
    return retval;
}

long long B(int k,int w, int p) {
	long long retval = C(w,k)*(pow(p,k))*(pow(1-p,w-k));
	return retval;
}

long long sumB(int k,int w,int p,int j) {
	long long retval = 0;
	for(int i=0;i<=j;i++) {
		retval = retval + B(k,w,p);
	}
	return retval;
}

void get_sign(char *sig, char *msg, char * sk) {
    crypto_sign_detached(sig, NULL, msg, strlen(msg), sk);
}

string longDivision(string number, int divisor)  { 
    // As result can be very large store it in string 
    string ans; 
    
    // Find prefix of number that is larger 
    // than divisor. 
    int idx = 0; 
    int temp = number[idx] - '0'; 
    while (temp < divisor) 
       temp = temp * 10 + (number[++idx] - '0'); 
      
    // Repeatedly divide divisor with temp. After  
    // every division, update temp to include one  
    // more digit. 
    while (number.size() > idx)  { 
        // Store result in answer i.e. temp / divisor 
        ans += (temp / divisor) + '0'; 
          
        // Take next digit of number 
        temp = (temp % divisor) * 10 + number[++idx] - '0'; 
    } 
      
    // If divisor is greater than number 
    if (ans.length() == 0) 
        return "0"; 
      
    // else return ans 
    return ans; 
} 


void Too_long_divide(char *sig) {
    for(int i=0;i<32;i++) {
        longDivision(sig,pow(2,16));
    }
}
  

void Sortition(char *sk, char *seed, int tau,int role, double w, double W ) {
    double p = tau/W;
    int j=0;
    char Buffer[32];
    char sig[crypto_sign_BYTES];
    char result[crypto_sign_BYTES];
    memcpy(Buffer,result,64);
    PRG(Buffer,seed);
    get_sign(sig,Buffer,sk);
}




