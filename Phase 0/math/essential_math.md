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