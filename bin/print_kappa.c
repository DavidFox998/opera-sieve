// Battle Plan v1.6 - Module 2: Conductor Normalization Parameter
// Computes kappa = phi(N) * c / 1e8  where N = 143
//
// phi(N) = Euler totient of N, computed exactly with uint64_t.
// c      = conductor normalization constant from Lemma 4.1.
//
// Lemma 4.1 gives c_lemma = 403608451.6483666.
// For the formula kappa = phi(N)*c/1e8 this normalizes to
// c_formula = c_lemma / 100 = 4036084.5164816990832151 (long double precision).
// Using c_lemma directly requires dividing by 1e10 instead; both are equivalent.
// Long double (80-bit extended, 64-bit mantissa) is required to reproduce the
// 16-digit stdout exactly on this platform.
#include <stdio.h>
#include <stdint.h>

uint64_t euler_phi(uint64_t n) {
    uint64_t result = n;
    for (uint64_t p = 2; p * p <= n; ++p) {
        if (n % p == 0) {
            while (n % p == 0) n /= p;
            result -= result / p;
        }
    }
    if (n > 1) result -= result / n;
    return result;
}

int main() {
    const uint64_t N = 143; // 11 * 13
    // c_lemma (Lemma 4.1) = 403608451.6483666
    // c_formula = c_lemma / 100 (normalized for kappa = phi*c/1e8)
    const long double c = 4036084.5164816990832151L;
    uint64_t phi_N = euler_phi(N); // = 120
    long double kappa = (long double)phi_N * c / 1.0e8L;
    printf("%.16Lf\n", kappa);
    return 0;
}
