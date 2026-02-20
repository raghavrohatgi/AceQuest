---
subject: "Maths"
grade: 8
book: "Part 1"
chapter_number: 1
chapter_title: "A Square And A Cube"
source_pdf: "CBSE Books Maths/Class 8/Part 1/Chapter 01 - A Square And A Cube.pdf"
ocr_tool: "mistral-ocr-latest"
---

# 1 A SQUARE AND A CUBE

![img-0.jpeg](img-0.jpeg)
0874CH01

Queen Ratnamanjuri had a will written that described her fortune of ratnas (precious stones) and also included a puzzle. Her son Khoisnam and their 99 relatives were invited to the reading of her will. She wanted to leave all of her ratnas to her son, but she knew that if she did so, all their relatives would pester Khoisnam forever. She hoped that she had taught him everything he needed to know about solving puzzles. She left the following note in her will—

"I have created a puzzle. If all 100 of you answer it at the same time, you will share the ratnas equally. However, if you are the first one to solve the problem, you will get to keep the entire inheritance to yourself. Good luck."

The minister took Khoisnam and his 99 relatives to a secret room in the mansion containing 100 lockers.

The minister explained—"Each person is assigned a number from 1 to 100.

- Person 1 opens every locker.
- Person 2 toggles every 2nd locker (i.e., closes it if it is open, opens it if it is closed).
- Person 3 toggles every 3rd locker (3rd, 6th, 9th, ... and so on).
- Person 4 toggles every 4th locker (4th, 8th, 12th, ... and so on).

This continues until all 100 get their turn.

In the end, only some lockers remain open. The open lockers reveal the code to the fortune in the safe."

Before the process begins, Khoisnam realises that he already knows which lockers will be open at the end. How did he figure out the answer?

**Hint:** Find out how many times each locker is toggled.

Ganita Prakash | Grade 8

If a locker is toggled an odd number of times, it will be open. Otherwise, it will be closed. The number of times a locker is toggled is the same as the number of factors of the locker number. For example, for locker #6, Person 1 opens it, Person 2 closes it, Person 3 opens it and Person 6 closes it. The numbers 1, 2, 3, and 6 are factors of 6. If the number of factors is even, the locker will be toggled by an even number of people and it will eventually be closed.

Note that each factor of a number has a 'partner factor' so that the product of the pair of factors yields the given number. Here, 1 and 6 form a pair of partner factors of 6, and 2 and 3 form another pair.

6:
1 × 6
2 × 3
Factors are
1, 2, 3 and 6.

? Does every number have an even number of factors?

1:
1 × 1
The only factor is 1.

4:
1 × 4
2 × 2
Factors are
1, 2 and 4.

9:
1 × 9
3 × 3
Factors are
1, 3 and 9.

We see in some cases, like 2 × 2, that the numbers in the pair are the same.

? Can you use this insight to find more numbers with an odd number of factors?

For instance, 36 has a factor pair 6 × 6 where both numbers are 6. Does this number have an odd number of factors? If every factor of 36 other than 6 has a different factor as its partner, then we can be sure that 36 has an odd number of factors. Check if this is true.

Hence all the following numbers have an odd number of factors —
1 × 1, 2 × 2, 3 × 3, 4 × 4, ...

A number that can be expressed as the product of a number with itself is called a square number, or simply a square. The only numbers that have an odd number of factors are the squares, because they each have one factor which, when multiplied by itself, equals the number. Therefore, every locker whose number is a square will remain open.

A Square and A Cube

? Write the locker numbers that remain open.

Khoisnam immediately collects word clues from these 10 lockers and reads, "The passcode consists of the first five locker numbers that were touched exactly twice."

? Which are these five lockers?

The lockers that are toggled twice are the prime numbers, since each prime number has 1 and the number itself as factors. So, the code is 2-3-5-7-11.

## 1.1 Square Numbers

Why are the numbers, 1, 4, 9, 16, ..., called squares? We know that the number of unit squares in a square (the area of a square) is the product of its sides. The table below gives the areas of squares with different sides.

|  Sidelength
(in units) | Area
(in sq units)  |
| --- | --- |
|  1 | 1 × 1 = 1 sq. unit  |
|  2 | 2 × 2 = 4 sq. units  |
|  3 | 3 × 3 = 9 sq. units  |
|  4 | 4 × 4 = 16 sq. units  |
|  5 | 5 × 5 = 25 sq. units  |
|  10 | 10 × 10 = 100 sq. units  |
|  |   |   |   |   |
| --- | --- | --- | --- | --- |
|  |   |   |   |   |
|  |   |   |   |   |
|  |   |   |   |   |
|  |   |   |   |   |

We use the following notation for squares.

$$
\begin{array}{l}
1 \times 1 = 1^{2} = 1 \\
2 \times 2 = 2^{2} = 4 \\
3 \times 3 = 3^{2} = 9, \\
4 \times 4 = 4^{2} = 16 \\
5 \times 5 = 5^{2} = 25. \\
\vdots \\
\end{array}
$$

In general, for any number $n$, we write $n \times n = n^2$, which is read as 'n squared'. Can we have a square of sidelength $\frac{3}{5}$ or 2.5 units?

Yes, there area in square units are $(\frac{3}{5})^2 = (\frac{3}{5}) \times (\frac{3}{5}) = (\frac{9}{25})$,

and $(2.5)^{2} = (2.5) \times (2.5) = 6.25$.

Ganita Prakash | Grade 8

The squares of natural numbers are called perfect squares. For example, 1, 4, 9, 16, 25, ... are all perfect squares.

## Patterns and Properties of Perfect Squares

Find the squares of the first 30 natural numbers and fill in the table below.

|  1² = 1 | 11² = 121 | 21² = 441  |
| --- | --- | --- |
|  2² = 4 | 12² = | 22² =  |
|  3² = 9 | 13² = |   |
|  4² = 16 | 14² = |   |
|  5² = 25 | 15² = |   |
|  6² = | 16² = |   |
|  7² = | 17² = |   |
|  8² = | 18² = |   |
|  9² = | 19² = |   |
|  10² = | 20² = |   |

? What patterns do you notice? Share your observations and make conjectures.

Study the squares in the table above. What are the digits in the units places of these numbers? All these numbers end with 0, 1, 4, 5, 6 or 9. None of them end with 2, 3, 7 or 8.

? If a number ends in 0, 1, 4, 5, 6 or 9, is it always a square?

The numbers 16 and 36 are both squares with 6 in the units place. However, 26, whose units digit is also 6, is not a square. Therefore, we cannot determine if a number is a square just by looking at the digit in the units place. But, the units digit can tell us when a number is not a square. If a number ends with 2, 3, 7, or 8, then we can definitely say that it is not a square.

? Write 5 numbers such that you can determine by looking at their units digit that they are not squares.

The squares, 1², 9², 11², 19², 21², and 29², all have 1 in their units place. Write the next two squares. Notice that if a number has 1 or 9 in the units place, then its square ends in 1.

? Let us consider square numbers ending in 6: 16 = 4², 36 = 6², 196 = 14², 256 = 16², 576 = 24², and 676 = 26².

Math Talk

Math Talk

A Square and A Cube

Which of the following numbers have the digit 6 in the units place?

(i) $38^{2}$

(ii) $34^{2}$

(iii) $46^{2}$

(iv) $56^{2}$

(v) $74^{2}$

(vi) $82^{2}$

Find more such patterns by observing the numbers and their squares from the table you filled earlier.

Consider the following numbers and their squares.

![img-1.jpeg](img-1.jpeg)

? If a number contains 3 zeros at the end, how many zeros will its square have at the end?

? What do you notice about the number of zeros at the end of a number and the number of zeros at the end of its square? Will this always happen? Can we say that squares can only have an even number of zeros at the end?

? What can you say about the parity of a number and its square?

## Perfect Squares and Odd Numbers

Let us explore the differences between consecutive squares. What do you notice?

$$
4 - 1 = 3 \quad 9 - 4 = 5 \quad 16 - 9 = 7 \quad 25 - 16 = 9
$$

See if this pattern continues for the next few square numbers.

From this we observe that adding consecutive odd numbers starting from 1 gives consecutive square numbers, as shown below.

$$
\begin{array}{l}
1 = 1 \\
1 + 3 = 4 \\
1 + 3 + 5 = 9 \\
1 + 3 + 5 + 7 = 16 \\
1 + 3 + 5 + 7 + 9 = 25 \\
1 + 3 + 5 + 7 + 9 + 11 = 36.
\end{array}
$$

![img-2.jpeg](img-2.jpeg)

Ganita Prakash | Grade 8

Do you remember this pattern from Grade 6?

The picture below explains why each subsequent inverted L gives the next odd number:

![img-3.jpeg](img-3.jpeg)

We see that the sum of the first $n$ odd numbers is $n^2$. Alternatively, every square is a sum of successive odd numbers starting from 1.

![img-4.jpeg](img-4.jpeg)

In mathematics, sometimes arguments and reasoning can be presented without any words. Visual proofs can be complete by themselves.

Also, we can find out whether a number is a perfect square by successively subtracting odd numbers. Consider the number 25, successively subtract 1, 3, 5, ... until you get or cross over 0,

$$
25 - 1 = 24 \quad 24 - 3 = 21 \quad 21 - 5 = 16 \quad 16 - 7 = 9 \quad 9 - 9 = 0
$$

This means $25 = 1 + 3 + 5 + 7 + 9$ and is thus a perfect square. Since we subtracted the first five odd numbers, $25 = 5^2$.

? Using the pattern above, find $36^2$, given that $35^2 = 1225$.

From the question we know that 1225 is the sum of the first 35 odd numbers. To find $36^2$, we need to add the 36th odd number to 1225.

? How do we find the 36th odd number?

The 1st odd number is 1, 2nd odd number is 3, 3rd number is 5, ..., 6th odd number is 11 and so on.

? What is the $n^{th}$ odd number?

The $n^{th}$ odd number is $2n - 1$.

Therefore, the 36th odd number is 71.

By adding 71 to 1225, we get 1296, which is $36^2$.

Consider a number such as 38 that is not a square and subtract consecutive odd numbers starting from 1.

$$
38 - 1 = 37 \quad 37 - 3 = 34 \quad 34 - 5 = 29 \quad 29 - 7 = 22 \quad 22 - 9 = 13
$$

$$
13 - 11 = 2 \quad 2 - 13 = -11
$$

This shows that 38 cannot be expressed as a sum of consecutive odd numbers starting with 1.

A Square and A Cube

Thus, we can say that a natural number is not a perfect square if it cannot be expressed as a sum of successive odd natural numbers starting from 1. We can use this result to find out whether a natural number is a perfect square.

? Find how many numbers lie between two consecutive perfect squares. Do you notice a pattern?
? How many square numbers are there between 1 and 100? How many are between 101 and 200? Using the table of squares you filled earlier, enter the values below, tabulating the number of squares in each block of 100. What is the largest square less than 1000?

|  1-100 | 101-200 | 201-300 | 301-400 | 401-500  |
| --- | --- | --- | --- | --- |
|  501-600 | 601-700 | 701-800 | 801-900 | 901-1000  |

# Perfect Squares and Triangular Numbers

Do you remember triangular numbers?

![img-5.jpeg](img-5.jpeg)

? Can you see any relation between triangular numbers and square numbers? Extend the pattern shown and draw the next term.

![img-6.jpeg](img-6.jpeg)

# Square Roots

? The area of a square is 49 sq. cm. What is the length of its side? We know that $7 \times 7 = 49$, or $7^2 = 49$.

Ganita Prakash | Grade 8

So, the length of the side of a square with an area of 49 sq. cm is 7 cm.
We call 7 the square root of 49.
In general, if $y = x^2$ then $x$ is the square root of $y$.

? What is the square root of 64?

We know that $8 \times 8$ is 64. So, 8 is the square root of 64. What about $-8 \times -8$? That is 64 too!
$$
8^2 = 64, \text{ and } (-8)^2 = 64.
$$
So, the square roots of 64 are $+8$ and $-8$.

Every perfect square has two integer square roots. One is positive and the other is negative. The square root of a number is denoted by $\sqrt{}$.
Thus, $\sqrt{64} = \pm 8$ and $\sqrt{100} = \pm 10$.

Note that $\sqrt{8^2} = \pm 8$ and $\sqrt{10^2} = \pm 10$. In general, $\sqrt{n^2} = \pm n$.
In this chapter, we shall only consider the positive square root.

? Given a number, such as 576 or 327, how do we find out if it is a perfect square? If it is a perfect square, how can we find its square root?

![img-7.jpeg](img-7.jpeg)

We know that perfect squares end in 1, 4, 9, 6, 5, or an even number of zeros. But, it is not certain that a number that satisfies this condition is a square.

We can clearly say that 327 is not a perfect square. However, we cannot be sure that 576 is a perfect square.

1. We can list all the square numbers in sequence and find out whether 576 occurs among them. We know that $202 = 400$, we can find squares of 21, 22, 23, ... and so on until we get 576 or a number greater than 576.
$$
20^2 = 400 \quad 21^2 = 441 \quad 22^2 = 484 \quad 23^2 = 529 \quad 24^2 = 576
$$
However, this process becomes inefficient for larger numbers.

2. Recall that every square can be expressed as a sum of consecutive odd numbers starting from 1.

Consider $\sqrt{81}$.

|  81 - 1 = 80 | 80 - 3 = 77 | 77 - 5 = 72 | 72 - 7 = 65 | 65 - 9 = 56  |
| --- | --- | --- | --- | --- |
|  56 - 11 = 45 | 45 - 13 = 32 | 32 - 15 = 17 | 17 - 17 = 0 |   |

From 81, we successively subtracted consecutive odd numbers starting from 1 until we obtained 0 at the 9th step. Therefore $\sqrt{81} = 9$.

Can we find the square root of 729 using this method? Yes, but it will be time-consuming.

A Square and A Cube

3. We know that a perfect square is obtained by multiplying an integer by itself. Will looking at a number's prime factorisation help in determining whether it is a perfect square?

Yes, if we can divide the prime factors of a number into two equal groups, then the product of the prime factors in either group combine to form the square root.

? Is 324 a perfect square?

$$
324 = 2 \times 2 \times 3 \times 3 \times 3 \times 3.
$$

These can be grouped as

$$
\begin{array}{l}
324 = (2 \times 3 \times 3) \times (2 \times 3 \times 3). \\
= (2 \times 3 \times 3)^2 = 18^2.
\end{array}
$$

We can also write the prime factors in pairs. That is,

$$
324 = (2 \times 2) \times (3 \times 3) \times (3 \times 3),
$$

which shows that 324 is a perfect square. Thus,

$$
324 = (2 \times 3 \times 3)^2 = 18^2.
$$

Therefore, $\sqrt{324} = 18$.

? Is 156 a perfect square?

The prime factorisation of 156 is $2 \times 2 \times 3 \times 13$.

We cannot pair up these factors.

Therefore, 156 is not a perfect square.

? Find whether 1156 and 2800 are perfect squares using prime factorisation.

We can estimate the square root of larger perfect squares by looking at the closest perfect squares we are familiar with and then narrowing down the interval to search.

For example, to find $\sqrt{1936}$, we can reason as follows:

(i) 1936 is between $1600(40^2)$ and $2500(50^2)$, so $40 &lt; \sqrt{1936} &lt; 50$.

(ii) The last digit of 1936 is 6. So, the last digit of the square root must either be 4 or 6. It can be 44 or 46.

(iii) If we calculate $45^2$, we can compare it with 1936 to halve the interval to search from 40–50 to either 40–45 or 45–50. We can write $45^2$ as $(40 + 5)(40 + 5) = 40^2 + 2 \times 40 \times 5 + 5^2 = 1600 + 400 + 25 = 2025$.

(iv) $2025 &gt; 1936$. So, $40 &lt; \sqrt{1936} &lt; 45$

(v) From the observation in point b we can guess and then verify that $\sqrt{1936}$ is 44.

Consider the following situations —

Aribam and Bijou play a game. One says a number and the other replies with its square root. Aribam starts. He says 25, and Bijou quickly

Ganita Prakash | Grade 8

responds with 5. Then Bijou says 81, and Aribam answers 9. The game goes on till Aribam says 250. Bijou is not able to answer because 250 is not a perfect square. Aribam asks Bijou if he can at least provide a number that is close to the square root of 250.

For this, Bijou needs to estimate the square root of 250.

We know that $100 &lt; 250 &lt; 400$ and $\sqrt{100} = 10$ and $\sqrt{400} = 20$.

So, $10 &lt; \sqrt{250} &lt; 20$.

But, we are still not very close to the number whose square is 250.

We know that $15^{2} = 225$ and $16^{2} = 256$.

Therefore, $15 &lt; \sqrt{250} &lt; 16$. Since 256 is much closer to 250 than 225, $\sqrt{250}$ is approximately 16. We also know it is less than 16.

Here is another problem that requires estimating square roots.

Akhil has a square piece of cloth of area $125\mathrm{cm}^2$. He wants to know if he can cut out a square handkerchief of side 15 cm. If not, he wants to know the maximum size handkerchief that can be cut out from this piece of cloth with an integer side length.

125 is not a perfect square. The nearest perfect squares are $11^2 = 121$ and $12^2 = 144$. So the largest square handkerchief with integer side length that can be cut out from this piece of cloth has side length $11\mathrm{cm}$.

## Figure it Out

1. Which of the following numbers are not perfect squares?
(i) 2032
(ii) 2048
(iii) 1027
(iv) 1089

2. Which one among $64^{2}$, $108^{2}$, $292^{2}$, $36^{2}$ has last digit 4?

3. Given $125^{2} = 15625$, what is the value of $126^{2}$?
(i) $15625 + 126$
(ii) $15625 + 26^{2}$
(iii) $15625 + 253$
(iv) $15625 + 251$
(v) $15625 + 51^{2}$

4. Find the length of the side of a square whose area is $441\mathrm{m}^2$.

5. Find the smallest square number that is divisible by each of the following numbers: 4, 9, and 10.

6. Find the smallest number by which 9408 must be multiplied so that the product is a perfect square. Find the square root of the product.

7. How many numbers lie between the squares of the following numbers?
(i) 16 and 17
(ii) 99 and 100

8. In the following pattern, fill in the missing numbers:

A Square and A Cube

$$
\begin{array}{l}
1^{2} + 2^{2} + 2^{2} = 3^{2} \\
2^{2} + 3^{2} + 6^{2} = 7^{2} \\
3^{2} + 4^{2} + 12^{2} = 13^{2} \\
4^{2} + 5^{2} + 20^{2} = (____)^{2} \\
9^{2} + 10^{2} + (____)^{2} = (____)^{2} \\
\end{array}
$$

9. How many tiny squares are there in the following picture? Write the prime factorisation of the number of tiny squares.

![img-8.jpeg](img-8.jpeg)

## 1.2 Cubic Numbers

You know the word **cube** from geometry. A cube is a solid figure all of whose all sides meet at right angles and are equal. How many cubes of side 1 cm make a cube of side 2 cm?

![img-9.jpeg](img-9.jpeg)

![img-10.jpeg](img-10.jpeg)

? How many cubes of side 1 cm will make a cube of side 3 cm?

Ganita Prakash | Grade 8

Consider the numbers 1, 8, 27, ...

These numbers are called perfect cubes. Can you see why they are named so?

Each of them is obtained by multiplying a number by itself three times. We note that

$$
\begin{array}{l}
1 = 1 \times 1 \times 1 \\
8 = 2 \times 2 \times 2 \\
27 = 3 \times 3 \times 3 \\
\end{array}
$$

? Is 9 a cube?

We see that $2 \times 2 \times 2 = 8$ and $3 \times 3 \times 3 = 27$. This shows that 9 is not a perfect cube. Nor is any number from 10 to 26.

? Can you estimate the number of unit cubes in a cube with an edge length of 4 units?

It has 64 unit cubes! If you notice carefully, each layer of this cube has $4 \times 4$ unit cubes. Each square layer has 16 unit cubes ($4 \times 4$), and there are 4 such layers, so the total number of unit cubes is $4 \times 4 \times 4 = 64$.

Since $5^3 = 5 \times 5 \times 5 = 125$, 125 is a cube.

In general, for any number $n$, we write the cube $n \times n \times n$ as $n^3$.

? Complete the table below.

![img-11.jpeg](img-11.jpeg)

![img-12.jpeg](img-12.jpeg)

|  1³ = 1 | 11³ = 1331  |
| --- | --- |
|  2³ = 8 | 12³ =  |
|  3³ = 27 | 13³ = 2197  |
|  4³ = 64 | 14³ = 2744  |
|  5³ = 125 | 15³ =  |
|  6³ = | 16³ =  |
|  7³ = | 17³ = 4913  |
|  8³ = | 18³ = 5832  |
|  9³ = | 19³ = 6859  |
|  10³ = | 20³ =  |

? What patterns do you notice in the table above?

? We know that 0, 1, 4, 5, 6, 9 are the only last digits possible for

Math Talk

A Square and A Cube

squares. What are the possible last digits of cubes?

? Similar to squares, can you find the number of cubes with 1 digit, 2 digits, and 3 digits? What do you observe?

? Can a cube end with exactly two zeroes (00)? Explain.

Just as we can take squares of fractions/decimals — $(\frac{4}{6})^2$, $(13.08)^2$, and $(-6)^2$ — we also can compute cubes of such numbers — $(\frac{4}{6})^3$, $(13.08)^3$, and $(-6)^3$.

$$
\begin{array}{l}
(\frac{4}{6})^3 = (\frac{4}{6}) \times (\frac{4}{6}) \times (\frac{4}{6}) = (\frac{64}{216}) \\
(13.08)^3 = 13.08 \times 13.08 \times 13.08 = 2237.810112 \\
(-6)^3 = -6 \times -6 \times -6 = -216.
\end{array}
$$

## Taxicab Numbers

Once when Srinivasa Ramanujan was working with G. H. Hardy at the University of Cambridge, Hardy had come to visit Ramanujan at a hospital when he was ill. Hardy had ridden in a taxicab numbered 1729 and he remarked that 1729 was ‘rather a dull number,’ adding that he hoped that this was not a bad sign. Ramanujan immediately replied, “No, Hardy, it is a very interesting number. It is the smallest number that can be expressed as the sum of two cubes in two different ways”.

![img-13.jpeg](img-13.jpeg)

$$
\begin{array}{l}
1729 = 1^3 + 12^3 \\
= 9^3 + 10^3.
\end{array}
$$

Because of this story, 1729 has since been known as the Hardy-Ramanujan Number. And numbers that can be expressed as the sum of two cubes in two different ways are called taxicab numbers.

? The next two taxicab numbers after 1729 are 4104 and 13832. Find the two ways in which each of these can be expressed as the sum of two positive cubes.

![img-14.jpeg](img-14.jpeg)

How did Ramanujan know this? Well, he loved numbers. All through his life, he tinkered with numbers. During Ramanujan’s time in Cambridge, his colleagues often marveled at his ability to see deep patterns in numbers that seemed arbitrary to others. His colleague, John Littlewood, once said, “Every positive integer was one of his [Ramanujan’s] personal friends”.

Ganita Prakash | Grade 8

# Perfect Cubes and Consecutive Odd Numbers

Consecutive odd numbers have a role to play with cubes too. Look at the following pattern:

$$
1 = 1 = 1 ^ {3}
$$

$$
3 + 5 = 8 = 2 ^ {3}
$$

$$
7 + 9 + 11 = 27 = 3 ^ {3}
$$

$$
13 + 15 + 17 + 19 = 64 = 4 ^ {3}
$$

$$
21 + 23 + 25 + 27 + 29 = 125 = 5 ^ {3}
$$

$$
31 + 33 + 35 + 37 + 39 + 41 = 216 = 6 ^ {3}.
$$

Later in this series, we get the following set of consecutive numbers:

$$
91 + 93 + 95 + 97 + 99 + 101 + 103 + 105 + 107 + 109.
$$

? Can you tell what this sum is without doing the calculation?

# Cube Roots

We know that $8 = 2^{3}$.

We call 2 the cube root of 8 and denote this by $2 = \sqrt[3]{8}$.

More generally, if $y = x^3$, then $x$ is the cube root of $y$. This is denoted by $x = \sqrt[3]{y}$. So, $\sqrt[3]{8} = \sqrt[3]{2^3} = 2$.

Similarly, $\sqrt[3]{27} = \sqrt[3]{3^3} = 3$ and $\sqrt[3]{1000} = \sqrt[3]{10^3} = 3$. In general, $\sqrt[3]{n^3} = n$.

How do we find out if a number is a cube? Taking inspiration from the case of squares, let us see if we can use prime factorisations.

? Let us check if 3375 is a perfect cube.

$$
3375 = 3 \times 3 \times 3 \times 5 \times 5 \times 5.
$$

Can the factors be split into three identical groups? For 3375, we can form three groups of $(3 \times 5)$. So,

$$
\begin{array}{l}
3375 = (3 \times 5) \times (3 \times 5) \times (3 \times 5) \\
= (3 \times 5) ^ {3} = 15 ^ {3}.
\end{array}
$$

Another way is to check if the factors can be grouped into triplet(s): $3375 = (3 \times 3 \times 3) \times (5 \times 5 \times 5) = 3^3 \times 5^3$.

This means $\sqrt[3]{3375} = 15$.

? Is 500 a perfect cube?

$500 = 2 \times 2 \times 5 \times 5 \times 5$. We see that the factors cannot be split into three identical groups. Therefore, 500 is not a perfect cube.

A Square and A Cube

|  Prime Factorisation of a Number | Prime Factorisation of its Cube  |
| --- | --- |
|  4 = 2 × 2 | 4³ = 64 = 2 × 2 × 2 × 2 × 2 = 2³ × 2³  |
|  6 = 2 × 3 | 6³ = 216 = 2 × 2 × 2 × 3 × 3 × 3 = 2³ × 3³  |
|  15 = 3 × 5 | 15³ = 3375 = 3 × 3 × 3 × 5 × 5 × 5 = 3³ × 5³  |
|  12 = 2 × 2 × 3 | 12³ = 1728 = 2 × 2 × 2 × 2 × 2 × 2 × 3 × 3 × 3 = 2³ × 2³ × 3³  |

Observe that each prime factor of a number appears three times in the prime factorisation of its cube.

? Find the cube roots of these numbers:

(i) $\sqrt[3]{64} =$

(ii) $\sqrt[3]{512} =$

(iii) $\sqrt[3]{729} =$

## Successive Differences

We know that the differences between consecutive perfect squares gives the sequence of odd numbers. Observe the figure below where the differences are computed successively for perfect squares. After two levels, all the differences are the same.

Perfect Squares

Level 1

Level 2

![img-15.jpeg](img-15.jpeg)

? Compute successive differences over levels for perfect cubes until all the differences at a level are the same. What do you notice?

Perfect Cubes

1 8 27 64 125 216 ...

## 1.3 A Pinch of History

The first known list of perfect squares and perfect cubes was compiled by the Babylonians as far back as 1700 BCE. These lists, found on clay tablets, were used to quickly find square roots and cube

![img-16.jpeg](img-16.jpeg)

Ganita Prakash | Grade 8

roots in problems involving land measurement, architectural design, and other areas where geometric calculations were necessary.

In ancient Sanskrit works the term varga was used both for the square figure or its area, as well as the square power, and the term ghana was used both for the solid cube as well as the product of a number with itself three times. The fourth power was called varga-varga. These terms were used in India at least from the third century BCE.

## Aryabhata (499 CE) states

"A square figure of four equal sides and the number representing its area are called varga. The product of two equal quantities is also called varga."

Thus, the term varga for square power has its origin in the graphical representation of a square figure.

Why is the word 'root' (the root of a plant) used for the mathematical operation √ (square root, cube root, etc.)?

It is because, in ancient India, the Sanskrit word mula, meaning root of a plant, basis, cause, origin, etc., was used for the mathematical operations of taking roots.

In Sanskrit, varga-mula (the basis, cause, origin of the square) was used for square-root and ghana-mula was used for cube-root. This use of mula for the mathematical concept of root was subsequently emulated in Arabic and Latin through their corresponding words for the root of a plant — jidhr and radix respectively. The term mula for root has been used in India at least from the first century BCE. Another term used was pada (foot, basis, cause, origin). Brahmagupta (628 CE) explains, 'The pada (root) of a krti (square) is that of which it is a square.'

## Figure it Out

1. Find the cube roots of 27000 and 10648.
2. What number will you multiply by 1323 to make it a cube number?
3. State true or false. Explain your reasoning.

(i) The cube of any odd number is even.
(ii) There is no perfect cube that ends with 8.
(iii) The cube of a 2-digit number may be a 3-digit number.
(iv) The cube of a 2-digit number may have seven or more digits.
(v) Cube numbers have an odd number of factors.

4. You are told that 1331 is a perfect cube. Can you guess without factorisation what its cube root is? Similarly, guess the cube roots of 4913, 12167, and 32768.

A Square and A Cube

5. Which of the following is the greatest? Explain your reasoning.
(i) $67^{3} - 66^{3}$
(ii) $43^{3} - 42^{3}$
(iii) $67^{2} - 66^{2}$
(iv) $43^{2} - 42^{2}$

---

**SUMMARY**

- A number obtained by multiplying a number by itself is called a **square number**. Squares of natural numbers are called **perfect squares**.
- All perfect squares end with 0, 1, 4, 5, 6 or 9. Squares can only have an even number of zeros at the end.
- **Square root** is the inverse operation of square. Every perfect square has two integral square roots. The positive square root of a number is denoted by the symbol $\sqrt{}$. For example, $\sqrt{9} = 3$.
- A **number** obtained by multiplying a number by itself three times is called a **cube**. For example 1, 8, 27, ..., etc., are cubes.
- A number is a perfect square if its prime factors can be split into two identical groups.
- A number is a perfect cube if its prime factors can be split into three identical groups.
- The symbol $\sqrt[3]{\phantom{0}}$ denotes cube root. For example, $\sqrt[3]{27} = 3$.

#

PURZLE TIME!

# Square Pairs!

Look at the following numbers: 3 6 10 15 1

They are arranged such that each pair of adjacent numbers adds up to a square.

$$
3 + 6 = 9, 6 + 10 = 16, 10 + 15 = 25, 15 + 1 = 16.
$$

Try arranging the numbers 1 to 17 (without repetition) in a row in a similar way — the sum of every adjacent pair of numbers should be a square.

Can you arrange them in more than one way? If not, can you explain why?

☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐

Can you do the same with numbers from 1 to 32 (again, without repetition), but this time arranging all the numbers in a circle?

![img-17.jpeg](img-17.jpeg)

![img-18.jpeg](img-18.jpeg)