# Essential Math for solving ML problems

## Distributions

Two types of distrutions:

- Discrete: countable values, specific probability of single values
  - Counting: **binomial** -> how many sucesses in n trials?
  - Waiting: **geometric** -> how mant trials UNTIL first success?

- Continous: range of inifinite values, probability is single value is 0, they apply to ranges
  - Poisson: how many events in a fixed window?
  - Exponential: how long until first event?

---
Let's start by Discrete.

Bernoulli: binomial with n = 1 (single trial)

P(x=1) = p, P(x=0) = 1-p

PMF form: p^x (1-p)^(1-x)

Mean = p, Var = p(1-p)
Proof:
E[X] = 1*p + 0(1-p) = p+0 = p
E[X^2] = p^2, Var = E[X^2] - E[X]^2 = p-p^2 = p(1-p)

> For any binary variable X (0 or 1) X^2 = X so E[X^2] = E[X]

Binomial: sum of n independent bernouli trials,

$$
P(X=k)=\binom{n}{k}p^k(1-p)^{n-k}
$$

> this just means every sequence with k sucesses has same probability p^k * (1-p)^n-k and there are C(n, k) such sequences, intuitive.

Binomial theorem comes from this:

$$
(a+b)^n = \sum_{k=0}^{n} \binom{n}{k} a^{n-k}b^k
$$

Can verifyt if adding p^k and (1-p)^k to this, will give 1^n = 1

Intuitively again, E[X] = np and Var[X] = np(1-p) 

> Xi are independent.

If a random variable is sum of lots of bool variables, split sum before taking expectation

Question: flip a coin n times, Xi = 1 if i is heads, 0 otherwise
Total heads = X = x1+x2+..xn
Caluclate expectation of X squared... and not execpected value of X, squared. On average, what is the square of the number of successes?

Solving it: X^2 = (X1+X2..)^2, expand it!! **trick**
Seperate terms where indices are same, and terms where they're different

$$
X^2=\left(\sum_i X_i\right)^2=\sum_i X_i^2+\sum_{i\neq j}X_iX_j
$$

This makes computing expectation easy:
Because Xi is 0 or 1, Xi^2 = Xi, and all Xi behave same, you're doing this n times so it's just n*E[X] and for E[Xi*Xj]
$$
\mathbb E[X^2]=\sum_i\mathbb E[X_i]+\sum_{i\neq j}\mathbb E[X_iX_j]=n\mathbb E[X_i]+n(n-1)\mathbb E[X_iX_j]
$$