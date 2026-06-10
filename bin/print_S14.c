/* Battle Plan v1.6 - Module 4
 * S_14: primes p <= 10^4000 with ||p * alpha0|| < 1/p, alpha0 = 299 + pi/10
 * Numbers are printed as string literals because they exceed 64-bit range.
 * Output: 14 primes, comma-separated, single newline. */
#include <stdio.h>

int main(void) {
    const char *S14[14] = {
        "2",
        "3",
        "19",
        "191",
        "3993746143633",
        "3224057731518397",
        "631474305334326148720631",
        "154837899060399532100017991",
        "5041018329913599611229009621",
        "18862166390550560818837358289",
        "459626009549584478734178019503",
        "15293206459157399036476434739",
        "116526970762921198119897013559",
        "3494164289073996361661384853541"
    };
    for (int i = 0; i < 14; i++) {
        if (i > 0) printf(",");
        printf("%s", S14[i]);
    }
    printf("\n");
    return 0;
}
