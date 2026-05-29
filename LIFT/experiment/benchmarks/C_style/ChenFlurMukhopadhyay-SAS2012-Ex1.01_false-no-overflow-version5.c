extern int __VERIFIER_nondet_int(void);

int main() {
    int x, y;
    x = __VERIFIER_nondet_int();
    y = __VERIFIER_nondet_int();
    if (x <= 0 || y <= 0) return 0;

    while (x > 0) {
        x = -5*x - 6*y + 18;
    }
    return 0;
}
