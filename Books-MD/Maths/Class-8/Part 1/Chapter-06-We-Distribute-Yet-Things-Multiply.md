---
subject: "Maths"
grade: 8
book: "Part 1"
chapter_number: 6
chapter_title: "We Distribute, Yet Things Multiply"
source_pdf: "CBSE Books Maths/Class 8/Part 1/Chapter 06 - We Distribute, Yet Things Multiply.pdf"
ocr_tool: "mistral-ocr-latest"
---

WE DISTRIBUTE, YET THINGS MULTIPLY

USTACHED

We have seen how algebra makes use of letter symbols to write general statements about patterns and relations in a compact manner. Algebra can also be used to justify or prove claims and conjectures (like the many properties you saw in the previous chapter) and to solve problems of various kinds.

Distributivity is a property relating multiplication and addition that is captured concisely using algebra. In this chapter, we explore different types of multiplication patterns and show how they can be described in the language of algebra by making use of distributivity.

## 6.1 Some Properties of Multiplication

### Increments in Products

Consider the multiplication of two numbers, say, $23 \times 27$.

1. By how much does the product increase if the first number (23) is increased by 1?
2. What if the second number (27) is increased by 1?
3. How about when both numbers are increased by 1?
4. Do you see a pattern that could help generalise our observations to the product of any two numbers?

Let us first consider a simpler problem—find the increase in the product when 27 is increased by 1. From the definition of multiplication (and the commutative property), it is clear that the product increases by 23. This can be seen from the distributive property of multiplication as well. If $a, b$ and $c$ are three numbers, then—

We Distribute, Yet Things Multiply

$$
\widehat{a(b + c)} = ab + ac
$$

This property can be visualised nicely using a diagram:

![img-0.jpeg](img-0.jpeg)

This is called the distributive property of multiplication over addition. Using the identity $a(b + c) = ab + ac$ with $a = 23$, $b = 27$, and $c = 1$, we have

$$
23(27 + 1) = 23 \times 27 + 23
$$

Remember that here, $a(b + c)$ and $23(27 + 1)$ mean $a \times (b + c)$, and $23 \times (27 + 1)$, respectively. We usually skip writing the '×' symbol before or after brackets, just as in the case of expressions like $5a$, $xy$, etc.

We can also similarly expand $(a + b)c$ using the distributive property as follows—

$$
\begin{array}{l}
(a + b)c = c(a + b) \text{ (commutativity of multiplication)} \\
= ca + cb \text{ (distributivity)} \\
= ac + bc \text{ (commutativity of multiplication)}
\end{array}
$$

We can use the distributive property to find, in general, how much a product increases if one or both the numbers in the product are increased by 1. Suppose the initial two numbers are $a$ and $b$. If one of the numbers, say $b$, is increased by 1, then we have—

$$
a(b + 1) = ab \times a
$$

Ncrease

Now let us see what happens if both numbers in a product are increased by 1. If in a product $ab$, both $a$ and $b$ are increased by 1, then we obtain $(a + 1)(b + 1)$.

Ganita Prakash | Grade 8

? How do we expand this?

Let us consider $(a + 1)$ as a single term. Then, by the distributive property, we have

$$
(a + 1)(b + 1) = (a + 1)b + (a + 1)1
$$

Again applying the distributive property, we obtain

$$
\begin{array}{l}
(a + 1)(b + 1) = \boxed{(a + 1)b + (a + 1)1} \\
= ab + \boxed{(b + a + 1)} \\
\text{Increase}
\end{array}
$$

If $a = 23$, and, $b = 27$, we get

$$
\begin{array}{l}
(23 + 1)(27 + 1) = (23 + 1)\boxed{27 + (23 + 1)1} \\
= 23 \times 27 + \boxed{(27 + 23 + 1)} \\
\text{Increase}
\end{array}
$$

Thus, the product $ab$ increases by $a + b + 1$ when each of $a$ and $b$ are increased by 1.

? What would we get if we had expanded $(a + 1)(b + 1)$ by first taking $(b + 1)$ as a single term? Try it?

? What happens when one of the numbers in a product is increased by 1 and the other is decreased by 1? Will there be any change in the product?

Let us again take the product $ab$ of two numbers $a$ and $b$. If $a$ is increased by 1 and $b$ is decreased by 1, then their product will be $(a + 1)(b - 1)$. Expanding this, we get

$$
\begin{array}{l}
(a + 1)(b - 1) = (a + 1)b - (a + 1)1 \\
= ab + \boxed{b - (a + 1)} \\
= ab + \boxed{\boxed{b - a - 1}} \\
\text{Increase}
\end{array}
$$

If $a = 23$, and $b = 27$, we get

$$
\begin{array}{l}
(23 + 1)(27 - 1) = (23 + 1)\boxed{27 - (23 + 1)1} \\
= 23 \times 27 + \boxed{27 - (23 + 1)} \\
= 23 \times 27 + \boxed{\boxed{27 - 23 - 1}} \\
\text{Increase}
\end{array}
$$

? Will the product always increase? Find 3 examples where the product decreases.

? What happens when $a$ and $b$ are negative integers?

Check by substituting different values for $a$ and $b$ in each of the above cases. For example, $a = -5$, $b = 8$; $a = -4$, $b = -5$; etc.

We have seen that integers also satisfy the distributive property, that is, if $x, y$ and $z$ are any three integers, then $x(y + z) = xy + xz$.

Thus, the expressions we have for increase of products hold when the letter-numbers take on negative integer values as well.

Recall that two algebraic expressions are equal if they take on the same values when their letter-numbers are replaced by numbers. These

We Distribute, Yet Things Multiply

numbers could be any integers. Mathematical statements that express the equality of two algebraic expressions, such as

$$
a (b + 8) = ab + 8a,
$$

$$
(a + 1)(b - 1) = ab + b - a - 1, \text{ etc.},
$$

are called identities.

By how much will the product of two numbers change if one of the numbers is increased by $m$ and the other by $n$?

If $a$ and $b$ are the initial numbers being multiplied, they become $a + m$ and $b + n$.

$$
\begin{array}{l}
(a + m)(b + n) = (a + m)b + (a + m)n \\
= ab + mb + an + mn
\end{array}
$$

The increase is $an + bm + mn$.

Notice that the product is the sum of the product of each term of $(a + m)$ with each term of $(b + n)$.

![img-1.jpeg](img-1.jpeg)

This identity can be visualised as follows—

![img-2.jpeg](img-2.jpeg)

$(a + m)(b + n)$

Ganita Prakash | Grade 8

? This identity can be used to find how products change when the numbers being multiplied are increased or decreased by any amount. Can you see how this identity can be used when one or both numbers are decreased?

For example, let us reconsider the case when one number is increased by 1 and the other decreased by 1. Let us write the product $(a + 1)(b - 1)$ as $(a + 1)(b + (-1)$. Taking $m = 1$ and $n = -1$ in Identity 1, we have

$$
ab + (1) \times b + a \times (-1) + (1) \times (-1) = ab + b - a - 1,
$$

which is the same expression that we obtain earlier.

? Use Identity 1 to find how the product changes when

(i) one number is decreased by 2 and the other increased by 3;
(ii) both numbers are decreased, one by 3 and the other by 4.

? Verify the answers by finding the products without converting the subtractions to additions.

Generalising this, we can find the product $(a + u)(b - v)$ as follows.

$$
\begin{array}{l}
(a + u)(b - v) = (a + u)b - (a + u)v \\
= ab + ub - (av + uv) \\
= ab + ub - av - uv.
\end{array}
$$

Check that this is the same as taking $m = u$ and $n = -v$ in Identity 1.

As in Identity 1, the product $(a + u)(b - v)$ is the sum of the product of each term of $a + u$ ($a$ and $u$) with each term of $b - v$ ($b$ and $(-v)$). Notice that the signs of the terms in the products can be determined using the usual rules of integer multiplication.

? See how the rules of integer multiplication allows us to handle multiple cases using a single identity!

? Expand (i) $(a - u)(b + v)$, (ii) $(a - u)(b - v)$.

We get

$$
\begin{array}{l}
(a - u)(b + v) = ab - ub + av - uv, \text{ and} \\
(a - u)(b - v) = ab - ub - av + uv.
\end{array}
$$

The distributive property is not restricted to two terms within a bracket.

? Example 1: Expand $\frac{3a}{2} (a - b + \frac{1}{5})$.

$$
\frac{3a}{2} (a - b + \frac{1}{5}) = (\frac{3a}{2} \times a) - (\frac{3a}{2} \times b) + (\frac{3a}{2} \times \frac{1}{5}).
$$

The terms can be simplified as follows—

$$
\frac{3a}{2} \times a = \frac{3}{2} \times (a \times a).
$$

We Distribute, Yet Things Multiply

Using exponent notation, we can write $\frac{3}{2} \times (a \times a) = \frac{3}{2} a^2$.

$$
\frac{3a}{2} \times b = \frac{3}{2} \times (a \times b) = \frac{3}{2} ab.
$$

$$
\frac{3a}{2} \times \frac{1}{5} = \left(\frac{3}{2} \times \frac{1}{5}\right) a = \frac{3}{10} a
$$

So we get

$$
\frac{3a}{2} (a - b + \frac{1}{5}) = \frac{3}{2} a^2 - \frac{3}{2} ab + \frac{3}{10} a.
$$

? Can any two terms be added to get a single term?

For example, can $\frac{3}{2} a^2$ and $\frac{3}{10} a$ be added to get a single term?

We see that no two terms have exactly the same letter-numbers, which would have allowed them to be simplified into a single term. So, a further simplification of the expression is not possible.

Recall that we call terms having the same letter-numbers like terms.

? Example 2: Expand $(a + b)(a + b)$.

We have $(a + b)(a + b) = (a + b)a + (a + b)b = a \times a + b \times a + ab + b \times b$

$$
= a^2 + ba + ab + b^2
$$

Since $ba = ab$, we have two terms having the same letter-numbers $ab$ (or, that are like terms), and so can be added —

$$
ba + ab = ab + ab = 2ab
$$

So we get

$$
(a + b)(a + b) = a^2 + 2ab + b^2.
$$

? Example 3: Expand $(a + b)(a^2 + 2ab + b^2)$.

$$
\begin{aligned}
(a + b)(a^2 + 2ab + b^2) &amp;= (a + b)a^2 + (a + b) \times 2ab + (a + b)b^2 \\
&amp;= (a \times a^2) + ba^2 + (a \times 2ab) + (b \times 2ab) + ab^2 + (b \times b^2)
\end{aligned}
$$

The terms can be simplified as follows—

$$
a \times a^2 = a^3 \text{ (why?)}
$$

$$
ba^2 = a^2b
$$

$$
a \times 2ab = 2 \times a \times a \times b = 2a^2b
$$

$$
b \times 2ab = 2 \times a \times b \times b = 2ab^2
$$

$$
b \times b^2 = b^3
$$

So, $(a + b)(a^2 + 2ab + b^2) = a^3 + a^2b + 2a^2b + 2ab^2 + ab^2 + b^3$.

We see that $a^2b$ and $2a^2b$ have the same letter-numbers (or, are like terms) and so can be added—

Ganita Prakash | Grade 8

$$
a^{2}b + 2a^{2}b = (1 + 2)a^{2}b = 3a^{2}b.
$$

Similarly, $ab^2$ and $2ab^2$ are like terms and so can be added—

$$
ab^2 + 2ab^2 = (1 + 2)ab^2 = 3ab^2.
$$

Thus, we have

$$
(a + b) \times (a^2 + 2ab + b^2) = a^3 + 3a^2b + 3ab^2 + b^3.
$$

## A Pinch of History

The distributive property of multiplication over addition was implicit in the calculations of mathematicians in many ancient civilisations, particularly in ancient Egypt, Mesopotamia, Greece, China, and India. For example, the mathematicians Euclid (in geometric form) and Āryabhāṭa (in algebraic form) used the distributive law in an implicit manner extensively in their mathematical and scientific works. The first explicit statement of the distributive property was given by Brahmagupta in his work *Brahmasphūṭasiddhānta* (Verse 12.55), who referred to the use of the property for multiplication as *khanda-guṇanam* (multiplication by parts). His verse states, “The multiplier is broken up into two or more parts whose sum is equal to it; the multiplicand is then multiplied by each of these and the results added”. That is, if there are two parts, then using letter symbols this is equivalent to the identity $(a + b)c = ac + bc$. In the next verse (Verse 12.56), Brahmagupta further describes a method for doing fast multiplication using this distributive property, which we explore further in the next section.

## Figure it Out

1. Observe the multiplication grid below. Each number inside the grid is formed by multiplying two numbers. If the middle number of a $3 \times 3$ frame is given by the expression $pq$, as shown in the figure, write the expressions for the other numbers in the grid.

|  x | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  1 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10  |
|  2 | 2 | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 18 | 20  |
|  3 | 3 | 6 | 9 | 12 | 15 | 18 | 21 | 24 | 27 | 30  |
|  4 | 4 | 8 | 12 | 16 | 20 | 24 | 28 | 32 | 36 | 40  |
|  5 | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50  |
|  6 | 6 | 12 | 18 | 24 | 30 | 36 | 42 | 48 | 54 | 60  |
|  7 | 7 | 14 | 21 | 28 | 35 | 42 | 49 | 56 | 63 | 70  |
|  8 | 8 | 16 | 24 | 32 | 40 | 48 | 56 | 64 | 72 | 80  |
|  9 | 9 | 18 | 27 | 36 | 45 | 54 | 63 | 72 | 81 | 90  |
|  10 | 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 | 90 | 100  |
|  3 × 5 | 3 × 6 | 3 × 7  |
| --- | --- | --- |
|  4 × 5 | 4 × 6 | 4 × 7  |
|  5 × 5 | 5 × 6 | 5 × 7  |
|  |   |   |
| --- | --- | --- |
|   | pq |   |
|  |   |   |

We Distribute, Yet Things Multiply

2. Expand the following products.

(i) $(3 + u)(v - 3)$
(ii) $\frac{2}{3} (15 + 6a)$
(iii) $(10a + b)(10c + d)$
(iv) $(3 - x)(x - 6)$
(v) $(-5a + b)(c + d)$
(vi) $(5 + z)(y + 9)$

3. Find 3 examples where the product of two numbers remains unchanged when one of them is increased by 2 and the other is decreased by 4.

4. Expand (i) $(a + ab - 3b^2)(4 + b)$, and (ii) $(4y + 7)(y + 11z - 3)$.

5. Expand (i) $(a - b)(a + b)$, (ii) $(a - b)(a^2 + ab + b^2)$ and (iii) $(a - b)(a^3 + a^2b + ab^2 + b^3)$, Do you see a pattern? What would be the next identity in the pattern that you see? Can you check it by expanding?

## Fast Multiplications Using the Distributive Property

The distributive property can be used to come up with quick methods of multiplication when certain types of numbers are multiplied.

## When one of the numbers is 11, 101, 1001, ...

? Use the following multiplications to find the product of a number with 11 in a single step.

(a) $3874 \times 11$
(b) $5678 \times 11$

Let us take the first multiplication.

$$
3874 \times 11 = 3874(10 + 1) = 38740 + 3874
$$

$$
+ \begin{array}{c} 38740 \\ 3874 \end{array}
$$

Notice how the digits are getting added.

Let us take a 4-digit number $dcba$, that is, the number that has $d$ in the thousands place, $c$ in the hundreds place, $b$ in the tens place and $a$ in the units place.

$$
dcba \times (10 + 1) = dcba \times 10 + dcba.
$$

This becomes

$$
\begin{array}{c c c c c c} &amp; d &amp; c &amp; b &amp; a &amp; o \\ + &amp; &amp; d &amp; c &amp; b &amp; a \\ \hline &amp; d &amp; (c + d) &amp; (b + c) &amp; (a + b) &amp; a \end{array}
$$

Ganita Prakash | Grade 8

This can be used to obtain the product in one line.

Step 1
Step 2
Step 3

$$
\frac{3874}{4} \times 11
$$

$$
\frac{3874}{14} \times 11
$$

$$
\frac{3874}{614} \times 11
$$

Step 4
Step 5

$$
\frac{3874}{2614} \times 11
$$

$$
\frac{3874}{42614} \times 11
$$

? Describe a general rule to multiply a number (of any number of digits) by 11 and write the product in one line.

Evaluate (i) $94 \times 11$, (ii) $495 \times 11$, (iii) $3279 \times 11$, (iv) $4791256 \times 11$.

? Can we come up with a similar rule for multiplying a number by 101?

? Multiply 3874 by 101.

Let us take a 4-digit number $dcba$.

$$
dcba \times 101 = dcba \times (100 + 1) = dcba \times 100 + dcba.
$$

This becomes

$$
\frac{+}{d} \quad \frac{c}{c} \quad \frac{b}{b + d} \quad \frac{a}{a} \quad \frac{c}{c} \quad \frac{b}{b} \quad \frac{a}{a}
$$

? Use this to multiply $3874 \times 101$ in one line.

? What could be a general rule to multiply a number by 101 and write the product in one line? Extend this rule for multiplication by 1001, 10001, ...

? Use this to find (i) $89 \times 101$, (ii) $949 \times 101$, (iii) $265831 \times 1001$, (iv) $1111 \times 1001$, (v) $9734 \times 99$ and (vi) $23478 \times 999$.

Such methods of applying the distributive property to easily multiply two numbers were discussed extensively in the ancient mathematical works of Brahmagupta (628 CE), Sridharacharya (750 CE) and Bhaskaracharya (Lilavati, 1150 CE). In his work Brahmasphutasiddhānta (Verse 12.56), Brahmagupta refers to such methods for fast multiplication using the distributive property as ista-gunana.

Math Talk

144

We Distribute, Yet Things Multiply

# 6.2 Special Cases of the Distributive Property

## Square of the Sum/Difference of Two Numbers

? The area of a square of sidelength 60 units is 3600 sq. units (60²) and that of a square of sidelength 5 units is 25 sq. units (5²). Can we use this to find the area of a square of sidelength 65 units?

A square of sidelength 65 can be split into 4 regions as shown in the figure—a square of sidelength 60, a square of sidelength 5, and two rectangles of sidelengths 60 and 5. The area of the square of sidelength 65 is the sum of the areas of all its constituent parts. Can you find the areas of the four parts in the figure above?

We get

$$
\begin{array}{l}
65^2 = (60 + 5)^2 = 60^2 + 5^2 + 2 \times (60 \times 5). \\
= 3600 + 25 + 600 = 4225 \text{ sq. units}.
\end{array}
$$

Let us multiply $(60 + 5) \times (60 + 5)$ using the distributive property.

$$
\begin{array}{l}
(60 + 5) \times (60 + 5) = 60 \times 60 + 5 \times 60 + 60 \times 5 + 5 \times 5 \\
= 60^2 + 2 \times (60 \times 5) + 5^2.
\end{array}
$$

![img-3.jpeg](img-3.jpeg)

? What if we write $65^2$ as $(30 + 35)^2$ or $(52 + 13)^2$? Draw the figures and check the area that you get.

Let us look at the general expression for the square of sum of two numbers, $(a + b)^2$.

![img-4.jpeg](img-4.jpeg)

Using the distributive property, $(a + b)^2$ can be expanded as

$$
\begin{array}{l}
(a + b) \times (a + b) = a \times a + a \times b + b \times a + b \times b \\
= a^2 + 2ab + b^2,
\end{array}
$$

as we had already seen in Example 2.

Identity 1A $(a + b)^2 = a^2 + 2ab + b^2$

? If $a$ and $b$ are any two integers, is $(a + b)^2$ always greater than $a^2 + b^2$? If not, when is it greater?

Math Talk

? Use Identity 1A to find the values of $104^2$, $37^2$. (Hint: Decompose 104 and 37 into sums or differences of numbers whose squares are easy to compute.)

Ganita Prakash | Grade 8

? Use Identity 1A to write the expressions for the following.

(i) $(m + 3)^2$

(ii) $(6 + p)^2$

? Expand $(6x + 5)^2$.

|  Using the Distributive Property | Using the Identity  |
| --- | --- |
|  $(6x + 5)^2 = (6x + 5)(6x + 5)$ | $(6x + 5)^2 = (6x)^2 + 5^2 + 2 \times (6x \times 5)$  |
|  $(6x \times 6x) + (5 \times 6x) + (6x \times 5) + 5 \times 5$ | $(6x \times 5)^2 = 36x^2 + 25 + 60x$.  |
|  $(6x)^2 + 2(6x \times 5) + 5^2$ |   |
|  $(6x^2 + 60x + 25)$ |   |

![img-5.jpeg](img-5.jpeg)

If you have difficulty remembering or using the general rule, you can just apply the distributive property to multiply and get the desired result.

? Expand $(3j + 2k)^2$ using both the identity and by applying the distributive property.

? Can we use $60^2 (=3600)$ and $5^2 (=25)$ to find the value of $(60 - 5)^2$ or $55^2$? Let us approach this through geometry by drawing a square of side length 55 sitting inside a square of sidelength 60.

Area of a square of sidelength 55 is $(60 - 5)^2 = 55^2$.

![img-6.jpeg](img-6.jpeg)

We can get the area of the square of sidelength 55 by taking the area of the square of sidelength 60 and removing the areas of the two rectangles of sidelengths 60 and 5, i.e., $60^2 - (60 \times 5) - (5 \times 60)$. By doing this, we remove the area of the small square of sidelength 5 twice. What can we do with this expression to get the actual area?

We can add back the area of the square of sidelength 5 to this expression. That way, we are only subtracting this area once.

We Distribute, Yet Things Multiply

So,

$$
\begin{array}{l}
(60 - 5)^2 = 60^2 - (60 \times 5) - (5 \times 60) + 5^2 \\
= 3600 - 300 - 300 + 25 \\
= 3025.
\end{array}
$$

The area of the square of sidelength 55 is 3025 sq. units.

We have seen what $(a + b)^2$ gives when expanded. What is the expansion of $(a - b)^2$?

Using the distributive property,

$$
\begin{array}{l}
(a - b)^2 = (a - b) \times (a - b) \\
= (a)^2 - b a - a b + (b)^2 \\
= a^2 - 2 a b + b^2.
\end{array}
$$

? We can also use the expansion of $(a + b)^2$ to find the expansion of $(a - b)^2$. Think how.

Hint: $(a - b)^2 = (a + (-b))^2$

We can now directly use the expansion of $(a + b)^2$

$$
(a + (-b)^2 = (a)^2 + (-b)^2 + 2 \times (a) \times (-b)
$$

**Identity 1B** $(a - b)^2 = a^2 + b^2 - 2ab$

? Find the general expansion of $(a - b)^2$ using geometry, as we did for $55^2$.

? Use the identity $(a - b)^2$ to find the values of (a) $99^2$ and (b) $58^2$.

? Expand the following using both Identity 1B and by applying the distributive property

(i) $(b - 6)^2$

(ii) $(-2a + 3)^2$

(iii) $(7y - \frac{3}{4z})^2$

## Investigating Patterns

### Pattern 1

Look at the following pattern.

$$
2 (2^2 + 1^2) = 3^2 + 1^2
$$

$$
2 (3^2 + 1^2) = 4^2 + 2^2
$$

$$
2 (6^2 + 5^2) = 11^2 + 1^2
$$

$$
2 (5^2 + 3^2) = 8^2 + 2^2.
$$

Ganita Prakash | Grade 8

? Take a pair of natural numbers. Calculate the sum of their squares. Can you write twice this sum as a sum of two squares?

Try this with other pairs of numbers. Have you figured out a pattern?

Notice that $2(5^2 + 6^2) = (6 + 5)^2 + (6 - 5)^2$.

? Do the identities below help in explaining the observed pattern?

$$
(a + b)^2 = a^2 + 2ab + b^2
$$

$$
(a - b)^2 = a^2 - 2ab + b^2
$$

$$
(a + b)^2 + (a - b)^2 = (a^2 + 2ab + b^2) + (a^2 - 2ab + b^2)
$$

Adding the like terms $a^2 + a^2 = 2a^2$, $b^2 + b^2 = 2b^2$ and $2ab - 2ab = 0$, we get

$$
2(a^2 + b^2) = (a + b)^2 + (a - b)^2.
$$

## Pattern 2

? Here is a related pattern. Try to describe the pattern using algebra to determine if the pattern always holds.

$$
\begin{array}{l}
9 \times 9 - 1 \times 1 = 10 \times 8 \\
8 \times 8 - 6 \times 6 = 14 \times 2 \\
7 \times 7 - 2 \times 2 = 9 \times 5 \\
10 \times 10 - 4 \times 4 = 14 \times 6 \\
\end{array}
$$

The pattern here appears to be $a^2 - b^2 = (a + b) \times (a - b)$.

Is this a true identity? Using the distributive property, we get

$$
(a + b) \times (a - b) = a^2 - ab + ba - a^2.
$$

Adding the like terms, $ab + (-ab) = 0$, we see that indeed

**Identity 1C** $(a + b) \times (a - b) = a^2 - b^2.$

You had seen this identity earlier in Figure it Out 5 (i).

? Use Identity 1C to calculate $98 \times 102$, and $45 \times 55$.

? Show that $(a + b) \times (a - b) = a^2 - b^2$ geometrically.

![img-7.jpeg](img-7.jpeg)

We Distribute, Yet Things Multiply

![img-8.jpeg](img-8.jpeg)
Hint:

Sridharacharya (750 CE) gave an interesting method to quickly compute the squares of numbers using Identity 1C! Consider the following modified form of this identity —

$$
a^{2} = (a + b)(a - b) + b^{2}
$$

? Why is this identity true?

Now, for example, $31^2$ can be found by taking $a = 31$ and $b = 1$.

$$
\begin{array}{l}
31^{2} = (31 + 1)(31 - 1) + 1^{2} \\
= 32 \times 30 + 1 \\
= 961.
\end{array}
$$

$197^{2}$ can be found by taking $a = 197$, and $b = 3$.

$$
\begin{array}{l}
197^{2} = (197 + 3)(197 - 3) + 3^{2} \\
= 200 \times 194 + 9 \\
= 38809.
\end{array}
$$

? Figure it Out

1. Which is greater: $(a - b)^2$ or $(b - a)^2$? Justify your answer.
2. Express 100 as the difference of two squares.
3. Find $406^2$, $72^2$, $145^2$, $1097^2$, and $124^2$ using the identities you have learnt so far.
4. Do Patterns 1 and 2 hold only for counting numbers? Do they hold for negative integers as well? What about fractions? Justify your answer.

Math Talk

149

Ganita Prakash | Grade 8

## 6.3 Mind the Mistake, Mend the Mistake

We have expanded and simplified some algebraic expressions below to their simplest forms.

(i) Check each of the simplifications and see if there is a mistake.
(ii) If there is a mistake, try to explain what could have gone wrong.
(iii) Then write the correct expression.

![img-9.jpeg](img-9.jpeg)

![img-10.jpeg](img-10.jpeg)

![img-11.jpeg](img-11.jpeg)

![img-12.jpeg](img-12.jpeg)

![img-13.jpeg](img-13.jpeg)

![img-14.jpeg](img-14.jpeg)

![img-15.jpeg](img-15.jpeg)

![img-16.jpeg](img-16.jpeg)

![img-17.jpeg](img-17.jpeg)

![img-18.jpeg](img-18.jpeg)

![img-19.jpeg](img-19.jpeg)

![img-20.jpeg](img-20.jpeg)

## 6.4 This Way or That Way, All Ways Lead to the Bay

Observe the pattern in the figure below. Draw the next figure in the sequence. How many circles does it have? How many total circles are there in Step 10? Write an expression for the number of circles in Step $k$.

![img-21.jpeg](img-21.jpeg)

![img-22.jpeg](img-22.jpeg)

There are many ways of interpreting this pattern. Here are some possibilities:

We Distribute, Yet Things Multiply

# Method 1

Step 1

Step 2

Step 3

Step 4

...

Step k

![img-23.jpeg](img-23.jpeg)

![img-24.jpeg](img-24.jpeg)

![img-25.jpeg](img-25.jpeg)

![img-26.jpeg](img-26.jpeg)

$$
\begin{array}{l} 2 ^ {2} - 1 \\ = (1 + 1) ^ {2} - 1 \end{array}
$$

$$
3 ^ {2} - 1
$$

$$
= (2 + 1) ^ {2} - 1
$$

$$
4 ^ {2} - 1
$$

$$
= (3 + 1) ^ {2} - 1
$$

$$
5 ^ {2} - 1
$$

$$
= (4 + 1) ^ {2} - 1
$$

$$
\dots
$$

$$
(k + 1) ^ {2} - 1
$$

# Method 2

Step 1

Step 2

Step 3

Step 4

...

Step k

![img-27.jpeg](img-27.jpeg)

![img-28.jpeg](img-28.jpeg)

![img-29.jpeg](img-29.jpeg)

![img-30.jpeg](img-30.jpeg)

$$
\begin{array}{l} 1 + 2 \times 1 \\ = 1 ^ {2} + 2 \times 1 \end{array}
$$

$$
2 ^ {2} + 2 \times 2
$$

$$
= 2 ^ {2} + 2 \times 2
$$

$$
3 ^ {2} + 2 \times 3
$$

$$
= 3 ^ {2} + 2 \times 3
$$

$$
4 ^ {2} + 2 \times 4
$$

$$
= 4 ^ {2} + 2 \times 4
$$

$$
\dots
$$

$$
k ^ {2} + 2 \times k
$$

# Method 3

Step 1

Step 2

Step 3

Step 4

...

Step k

![img-31.jpeg](img-31.jpeg)

![img-32.jpeg](img-32.jpeg)

![img-33.jpeg](img-33.jpeg)

![img-34.jpeg](img-34.jpeg)

$$
\dots
$$

$$
\begin{array}{l} 1 \times 2 + 1 \\ = 1 \times (1 + 1) + 1 \end{array}
$$

$$
2 \times 3 + 2
$$

$$
= 2 \times (2 + 1) + 2
$$

$$
3 \times 4 + 3
$$

$$
= 3 \times (3 + 1) + 3
$$

$$
4 \times 5 + 4
$$

$$
= 4 \times (4 + 1) + 4
$$

$$
\dots
$$

$$
k \times (k + 1) + k
$$

Ganita Prakash | Grade 8

# Method 4

Step 1

Step 2

Step 3

Step 4

Step  $k$

![img-35.jpeg](img-35.jpeg)

![img-36.jpeg](img-36.jpeg)

![img-37.jpeg](img-37.jpeg)

![img-38.jpeg](img-38.jpeg)

$$
1 \times 3 = 1 \times (1 + 2)
$$

$$
2 \times 4 = 2 \times (2 + 2)
$$

$$
3 \times 5 = 3 \times (3 + 2)
$$

$$
4 \times 6 = 4 \times (4 + 2)
$$

$$
\dots
$$

$$
k \times (k + 2)
$$

Does your method match any of these, or is it different? Each expression that we have identified appears different, but are they really different? Since they describe the same pattern, they should all be the same. Let us simplify each expression and find out.

$$
\begin{array}{l}
(k + 1)^2 - 1 \\
= k^2 + 1 + 2k - 1 \\
= k^2 + 2k
\end{array}
$$

$$
k^2 + 2 \times k
$$

$$
= k^2 + 2k
$$

$$
k \times (k + 1) + k
$$

$$
= k^2 + k + k
$$

$$
= k^2 + 2k
$$

$$
k \times (k + 2)
$$

$$
= k^2 + 2k
$$

When carried out correctly, all methods lead to the same answer; $k^2 + 2k$. The expression $k^2 + 2k$ gives the number of circles at Step $k$ of this pattern.

![img-39.jpeg](img-39.jpeg)

In Mathematics, there are often multiple ways of looking at a pattern, and different ways of approaching and solving the same problem. Finding such ways often requires a great deal of creativity and imagination! While one or two of the ways might be your favourite(s), it can be amusing and enriching to explore other ways as well.

? Use this formula to find the number of circles in Step 15.
? Consider the pattern made of square tiles in the picture below.

![img-40.jpeg](img-40.jpeg)

![img-41.jpeg](img-41.jpeg)

![img-42.jpeg](img-42.jpeg)

···

We Distribute, Yet Things Multiply

? How many square tiles are there in each figure?
? How many are there in Step 4 of the sequence? What about Step 10?
? Write an algebraic expression for the number of tiles in Step  $n$ . Share your methods with the class. Can you find more than one method to arrive at the answer?

![img-43.jpeg](img-43.jpeg)

? Find the area of the (interior) shaded region in the figure below. All four rectangles have the same dimensions.

# Tadang's method:

The total region is a square of side  $(m + n)$  with an area  $(m + n)^2$ .

Subtracting the area of four rectangles from the total area will give the area of the interior shaded region. That is,  $(m + n)^2 - 4mn$ .

# Yusuf's method:

The shaded region is a square with sidelength  $(n - m)$ . So, its area is  $(n - m)^2$ .

![img-44.jpeg](img-44.jpeg)

? By expanding both expressions, check that  $(m + n)^2 - 4mn = (n - m)^2$ .
? Find out the area of the region with slanting lines in the figure. All three rectangles have the same dimensions (Fig. 1).

![img-45.jpeg](img-45.jpeg)
Fig. 1

# Anusha's method:

Required area  $=$  Area (ABCD)-Area (EFGH)

Area of  $\mathrm{ABCD} = x^2$

Area of EFGH  $= xy$

Required area  $= x^{2} - xy$

![img-46.jpeg](img-46.jpeg)

# Vaishnavi's method:

$$
Q S = y + x + y
$$

$$
= x + 2 y.
$$

Area of PQSR  $= x(x + 2y)$

Required area  $=$  Area of PQSR - (area of the three rectangles)

$$
= x (x + 2 y) - 3 x y.
$$

![img-47.jpeg](img-47.jpeg)

Ganita Prakash | Grade 8

# Aditya's method:

The required area is 2 times the area of JKLM.

$$
J K = \frac {x - y}{2}, K M = x
$$

Area (JKML) = $x\left(\frac{x - y}{2}\right)$

Required area = $2 \times$ Area of JKML

$$
\begin{array}{l} = 2 x \left(\frac {x - y}{2}\right) \\ = x (x - y). \\ \end{array}
$$

![img-48.jpeg](img-48.jpeg)

? By expanding the expressions, verify that all three expressions are equivalent. If $x = 8$ and $y = 3$, find the area of the shaded region.

? Write an expression for the area of the dashed region in the figure below. Use more than one method to arrive at the answer. Substitute $p = 6$, $r = 3.5$, and $s = 9$, and calculate the area.

![img-49.jpeg](img-49.jpeg)

# ? Figure it Out

1. Compute these products using the suggested identity.

(i) $46^{2}$ using Identity 1A for $(a + b)^2$
(ii) $397 \times 403$ using Identity 1C for $(a + b)(a - b)$
(iii) $91^{2}$ using Identity 1B for $(a - b)^2$
(iv) $43 \times 45$ using Identity 1C for $(a + b)(a - b)$

2. Use either a suitable identity or the distributive property to find each of the following products.

(i) $(p - 1)(p + 11)$
(ii) $(3a - 9b)(3a + 9b)$
(iii) $-(2y + 5)(3y + 4)$
(iv) $(6x + 5y)^2$
(v) $(2x - \frac{1}{2})^2$
(vi) $(7p) \times (3r) \times (p + 2)$

We Distribute, Yet Things Multiply

3. For each statement identify the appropriate algebraic expression(s).

(i) Two more than a square number.

$$
2 + s \quad (s + 2) ^ {2} \quad s ^ {2} + 2 \quad s ^ {2} + 4 \quad 2 s ^ {2} \quad 2 ^ {2} s
$$

(ii) The sum of the squares of two consecutive numbers

$$
m ^ {2} + n ^ {2} \quad (m + n) ^ {2} \quad m ^ {2} + 1 \quad m ^ {2} + (m + 1) ^ {2}
$$

$$
m ^ {2} + (m - 1) ^ {2} \quad (m + (m + 1)) ^ {2} \quad (2 m) ^ {2} + (2 m + 1) ^ {2}
$$

4. Consider any 2 by 2 square of numbers in a calendar, as shown in the figure.

|  February  |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- |
|  Su | M | Tu | W | Th | F | Sa  |
|   |  |  |  |  |  | 1  |
|  2 | 3 | 4 | 5 | 6 | 7 | 8  |
|  9 | 10 | 11 | 12 | 13 | 14 | 15  |
|  16 | 17 | 18 | 19 | 20 | 21 | 22  |
|  23 | 24 | 25 | 26 | 27 | 28 |   |

Find products of numbers lying along each diagonal — $4 \times 12 = 48$, $5 \times 11 = 55$. Do this for the other 2 by 2 squares. What do you observe about the diagonal products? Explain why this happens.

**Matt Talk**

Hint: Label the numbers in each 2 by 2 square as

|  a | (a + 1)  |
| --- | --- |
|  a + 7 | (a + 8)  |

5. Verify which of the following statements are true.

(i) $(k + 1)(k + 2) - (k + 3)$ is always 2.
(ii) $(2q + 1)(2q - 3)$ is a multiple of 4.
(iii) Squares of even numbers are multiples of 4, and squares of odd numbers are 1 more than multiples of 8.
(iv) $(6n + 2)^{2} - (4n + 3)^{2}$ is 5 less than a square number.

6. A number leaves a remainder of 3 when divided by 7, and another number leaves a remainder of 5 when divided by 7. What is the remainder when their sum, difference, and product are divided by 7?

7. Choose three consecutive numbers, square the middle one, and subtract the product of the other two. Repeat the same with other

Ganita Prakash | Grade 8

sets of numbers. What pattern do you notice? How do we write this as an algebraic equation? Expand both sides of the equation to check that it is a true identity.

8. What is the algebraic expression describing the following steps—add any two numbers. Multiply this by half of the sum of the two numbers? Prove that this result will be half of the square of the sum of the two numbers.

9. Which is larger? Find out without fully computing the product.

(i) $14 \times 26$ or $16 \times 24$
(ii) $25 \times 75$ or $26 \times 74$

10. A tiny park is coming up in Dhauli. The plan is shown in the figure. The two square plots, each of area $g^2$ sq. ft., will have a green cover. All the remaining area is a walking path w ft. wide that needs to be tiled. Write an expression for the area that needs to be tiled.

![img-50.jpeg](img-50.jpeg)

11. For each pattern shown below,

(i) Draw the next figure in the sequence.
(ii) How many basic units are there in Step 10?
(iii) Write an expression to describe the number of basic units in Step y.

![img-51.jpeg](img-51.jpeg)

We Distribute, Yet Things Multiply

# SUMMARY

- We extended the distributive property to find the product of two expressions each of which has two terms. The general form for the same is $(a + b) \times (c + d) = ac + ad + bc + bd$.

- We saw some special cases of this identity.
- $(a + b)^2 = a^2 + 2ab + b^2$
- $(a - b)^2 = a^2 - 2ab + b^2$
- $(a + b)(a - b) = a^2 - b^2$.

- We considered different patterns, and explored how to understand them using algebra. We saw that, often, there are multiple ways to solve a problem and arrive at the same correct answer. Finding different methods to approach and solve the same problem is a creative process.

![img-52.jpeg](img-52.jpeg)

# Coin Conjoin

Arrange 10 coins in a triangle as shown in the figure below on the left. The task is to turn the triangle upside down by moving one coin at a time. How many moves are needed? What is the minimum number of moves?

A triangle of 3 coins can be inverted (turned upside down) with a single move, and a triangle of 6 coins can be inverted by moving 2 coins.

![img-53.jpeg](img-53.jpeg)

![img-54.jpeg](img-54.jpeg)

The 10-coin triangle can be flipped with just 3 moves; did you figure out how? Find out the minimum possible moves needed to flip the next bigger triangle having 15 coins. Try the same for bigger triangular numbers.

Is there a simple way to calculate the minimum number of coin moves needed for any such triangular arrangement?

![img-55.jpeg](img-55.jpeg)