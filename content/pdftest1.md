title: AsciiDots
tags: 
protected: True

#Overview
By Aaron Janse

AsciiDots is an esoteric programming language based on ascii art. In this language, ''dots'', represented by periods (<code>.</code>), travel down ascii art paths and undergo operations.

##Samples

Hello world:

<pre> .-$&quot;Hello, World!&quot;</pre>

Quine:

<pre> ($'.-#40-$_a#-#35-$_a#-#39-$_a#)</pre>
Counter:

<pre>     /1#-.
     |
   /-+-$#\
   | |   |
  [+]&lt;1#-*
   |     |
   \--&lt;--/
      |
      0
      #
      |
      .</pre>
Semi-compact factorial calculator:

<pre> /---------*--~-$#-&amp;
 | /--;---\| [!]-\
 | *------++--*#1/
 | | /1#\ ||
[*]*{-}-*~&lt;+*?#-.
 *-------+-&lt;/
 \-#0----/</pre>
Code-golfed counter (15 bytes):

<pre>/.*$#-\
\{+}1#/</pre>

##Implementation
The original implementation is written in Python and is [https://github.com/aaronduino/asciidots on Github]
It can be tried out online at [https://asciidots.herokuapp.com asciidots.herokuapp.com]

##Program Syntax

###Basics

###Starting a program

<code>.</code> (a period), or <code>•</code> (a bullet symbol), signifies the starting location of a ''dot'', the name for this language's information-carrying unit. Each dot is initialized with both an [[#addresses-and-values|address and value]] of <code>0</code>.

###Ending a program

Interpretation of a dots program ends when a dot passes over an <code>&amp;</code>. It also ends when all dots die (i.e. they all pass over the end of a path into nothingness)

###Comments

Everything after <code>``</code> (two back ticks) is a comment and is ignored by the interpreter

###Paths

<code>|</code> (vertical pipe symbol) is a vertical path that dots travel along<br> <code>-</code> is a horizontal path that dots travel along

''Note'': Only one path should be adjacent to a starting dot location, so that there is no question where it should go

Here's an example program that just starts then ends (note that programs aren't always written and run top-to-bottom):

<pre>. `` This is where the program starts
| `` The dot travels downwards
| `` Keep on going!
&amp; `` The program ends</pre>
Think as these two paths as mirrors:<br> <code>/</code><br> <code>\</code>

So... here's a more complex program demonstrating the use of paths (it still just starts then ends):

<pre>

/-&amp;         `` This is where the program ends!
|
\-\ /-\
  | | |
/-/ | \-\
\---/   |
        |
        \-. `` Here's where the program starts</pre>
==== Special Paths ====

<code>+</code> is the crossing of paths (they do not interact)

<code>&gt;</code> acts like a regular, 2-way, horizontal, path, except dots can be inserted into the path from the bottom or the top. Those dots will go to the right<br> <code>&lt;</code> does likewise except new dots go to the left<br> <code>^</code> (caret) does this but upwards<br> <code>v</code> (the lowercase letter 'v') does likewise but downwards

Here's a way to bounce a dot backwards along its original path using these symbols:

<pre>/-&gt;-- `` Input/output comes through here
| |
\-/</pre>
But there is an easier way to do that:

<code>(</code> reflects a dot backwards along its original path. It accepts dot coming from the left, and lets them pass through to the right<br> <code>)</code> does likewise but for the opposite direction

<code>*</code> duplicates a dot and distributes copies including the original dot to all attached paths except the origin of dot

Here's a fun example of using these special paths. Don't worry—we'll soon be able to do more than just start then end a program.

<pre>  /-\ /-&amp; `` End
  | | |
  \-+-v
    | | /-\
(-&lt;-/ | | |
  |   \-&lt;-/
  \-\
    |
    .    `` Start</pre>
###Addresses and Values

<code>@</code> sets the address to the value after it following the direction of the line<br> <code>#</code> does the same except it sets the value

###Interactive Console

<code>$</code> is the output console. If there are single/double quotation marks (<code>'</code> or <code>&quot;</code>), it outputs the text after it until there are closing quotation marks. <code>#</code> and <code>@</code> are substituted with the dot's value and address, respectively<br>     When <code>_</code> follows a <code>$</code>, the program does not end printing with a [https://en.wikipedia.org/wiki/Newline newline].<br>     When not in quotes, if a <code>a</code> comes before a <code>#</code> or <code>@</code> symbol, the value is converted to ascii before it is printed

Here's how to set and then print a dot's value:

<pre>  . `` This dot is the data carrier
  | `` Travel along these vertical paths
  # `` Set the value...
  3 ``   ... to 3
  | `` Continue down the path
  $ `` Output to the console...
  # ``   ... the dot's value</pre>
Here's our hello world again:

<pre>.-$&quot;Hello, World!&quot;</pre>
Here's how to print that character 'h' without a newline:

<pre>.-$_&quot;h&quot;</pre>
And this prints '%' using the ascii code 37:

<pre>.-#37-$a#</pre>
<code>?</code> is input from the console. It prompts the user for a value, and pauses until a value is entered in. It only runs after a <code>#</code> or <code>@</code> symbol<br>

<pre>  . `` Start
  |
  # `` Get ready to set the value
  ? `` Prompt the user
  |
  $
  # `` Print that value to the console
    `` Since the only dot goes off the end of the path, it dies. Since no dots are left, the program ends</pre>
###Control Flow

<code>~</code> (tilde) redirects dots going through it horizontally to the upward path if a dot waiting at the bottom has a value ''not'' equal to than <code>0</code>. Otherwise, the dot continues horizontally. If an exclamation point (<code>!</code>) is under it, then it redirects the dot upwards only if the value of the dot waiting ''is'' equal to zero.<br>     <code>!</code> acts like a pipe. Special function described above

This example prompts for a value then prints to the console whether the user provided value is equal to zero:

<pre>  /-$&quot;The value is not equal to zero&quot;
  |
.-~-$&quot;The value is equal to zero&quot;
  |
  ?
  #
  |
  .</pre>
###Operations

<code>[*]</code> multiplies the value that passes through vertically by the value that runs into it horizontally. When a dot arrive here, it waits for another dot to arrive from a perpendicular direction. When that dot arrives, the dot that arrived from the top or bottom has its value updated and it continues through the opposite side. The dot that passed through horizontally is deleted.<br> <code>{*}</code> does likewise except it multiplies the value that enters horizontally by the value that enters vertically. The resulting dot exits horizontally<br>

Other operations work similarly but with a different symbol in the middle. This is the key to these symbols:<br> <code>*</code>: multiplication<br> <code>/</code>: division<br> <code>÷</code>: also division<br> <code>+</code>: addition<br> <code>-</code>: subtraction<br> <code>%</code>: modulus<br> <code>^</code>: exponent<br> <code>&amp;</code>: boolean AND<br> <code>!</code>: boolean NOT<br> <code>o</code>: boolean OR<br> <code>x</code>: boolean XOR<br> <code>&gt;</code>: greater than<br> <code>≥</code>: greater than or equal to<br> <code>&lt;</code>: less than<br> <code>≤</code>: less than or equal to<br> <code>=</code>: equal to<br> <code>≠</code>: not equal to<br>

Boolean operations return a dot with a value of <code>1</code> if the expression evaluates to true and <code>0</code> if false.

These characters are only considered operators when located within brackets. When outside of brackets, symbols like <code>*</code> perform their regular functions as described earlier.

Example:

<pre>`` Simple subtraction:
``   (3 - 2 = 1)

   #
   $
   |
  [-]-2#-.
   |
   3
   #
   |
   .</pre>
Add two user inputted values together then output the sum:

<pre>.-#?-{+}-$#
      |
.-#?--/</pre>
###Warps

A warp is a character that teleports, or 'warps', a dot to the other occurrence of the same letter in the program.

Define warps at the beginning of the file by listing them after a <code>%$</code>. The <code>%$</code> must be at the beginning of the line.

Example:

<pre>%$A

.-#9-A `` Create a dot, set its value to 9, then warp it

A-$#   `` Print the dot's value (9)</pre>
Here's a fun example of using warps (although it is not very useful in this case)

<pre>
%$A

#  /-)
$  |
\&gt;-A
 \-3#-.

A-\
\-/
</pre>
###Libraries

Dots supports libraries! A library is a program that defines a character (usually a letter).

#####Using Libraries

A library can be imported by starting a line with <code>%!</code>, followed with the file name, followed with a single space and then the character that the library defines.

By default, all copies of the character lead to the same ([https://en.wikipedia.org/wiki/Singleton_pattern singleton]) library code. This can cause some unexpected behavior if the library returns an old dot, since that old dot will come out of the char that ''it'' came from.

Here's an example of importing the standard <code>for_in_range</code> library (located in the <code>libs</code> folder) as the character <code>f</code>:

<pre>%!for_in_range.dots f</pre>
The way to use a library varies. Inputs and outputs of the library are through the alias character.

For the <code>for_in_range</code> library, the inputs are defined as follows: The dot coming from the '''left''' side sets the starting value of the counter. The dot coming from the '''right''' side sets the end value of the counter.

And the outputs are as follows: A dot for each number within the range defined by the inputs is output from the '''top'''. When the loop is complete (the end value has been reached), a dot is output from the '''bottom'''.

Here is an example of outputting all the numbers between <code>1</code> and <code>100</code> to the console, then stopping the program:

<pre>%!for_in_range.dots f

         #
         $
         |
.-*-#1---f-\
  \-#100-+-/
         |
         &amp;</pre>
#####Creating Libraries

Each library defines a character that will act as a warp to &amp; from the library.

That can be done like so:

<pre>%^X `` X could be replaced with a different character, if so desired</pre>
It is recommended that you create warps for different sides of the char. Just look at the example code for the <code>val_to_addr.dots</code> library:


Here's the code for a library that accepts a dot coming from the left, sets its value to its address, and then outputs it to the right:

<pre>%^X
%$AB

B-X-A


A-*----@{+}-#0-B
  |      |
  \------/</pre>

##Interpretation

Each tick, the dots will travel along the lines until they hit a character that acts as a function of multiple dots (i.e. an operation character or a <code>~</code> character). The dot will stop if it goes on a path that it has already traversed in the same tick

Due to the fact that dots may be moving backwards down a line, if a number or system value (e.g. <code>?</code>) is seen without a preceding <code>@</code> or <code>#</code>, it will be ignored, along with any <code>@</code> or <code>#</code> immediately thereafter

##More Examples

Hello, World!<br>

<pre>.-$&quot;Hello, World!&quot;</pre>
<br> Counter:

<pre>     /1#-.
     |
   /-+-$#\
   | |   |
  [+]&lt;1#-*
   |     |
   \--&lt;--/
      |
      0
      #
      |
      .</pre>
<br>

Find prime numbers:<br>

<pre>%$T

        .
        |
        #
        3
        |
        @
        1
        |
/--*--*-&lt;--\
|  |  |   /+----\
|  #  |   v+-0@-~-\
|  2  | /-&gt;~*{%}/ |
|  |  | 1  |\-+---/
|  |  | @  ^\ |
\-{+}-+-*  01 |
      | |  ## |
      | v--*+-/
      | |  ||
    /-* |  *+--\
    | T |  ||  |
    # $ # /~/  |
    0 # 1 */   |
    | | | |    |
    \-&gt;-+-~----&lt;-#$-2#-.
        \-/


 /--------\
 T        |
 *--------~
 |        |
 \-*----@[=]
   |      |
   \--#1--/</pre>

-----

<br>

Print the Fibonacci Sequence:<br>

<pre>.-#1\
. /->\
>[+] |
\-*#$/</pre>

<br>

Print powers of 2:<br>
<pre> .-#2\
 /---v
[*]2#*
 \-#$/</pre>

<br>

And a game!

<pre>/-&quot;&quot;$-.
|
\--$&quot;Pick a number between 1 and 255 (inclusive)&quot;\
/------------------------------------------------/
\--$&quot;I will correctly guess that number after no more than 8 tries&quot;\
/---------------------------------------------------------------&quot;&quot;$/
\--$&quot;After each of my guesses, respond with: &quot;\
/---------------------------------------------/
\--$&quot;     '2' if I guess too high,&quot;\
/----------------------------------/
\--$&quot;     '1' if I guess too low,&quot;\
/---------------------------------/
\--$&quot;  or '0' if I guess correctly&quot;\
/----------------------------------/
|
|                             /-&gt;-\
|         /--------------\ /-[-]| |
#         |           /#1\-~--+[+]|
6         |          /*-{-}*  | | |
4  /2#\   |     /----~-----+--+-+-+-#7-$a_#-$&quot;I won! Good game!&quot;-&amp;
|/{÷}-*---*     *----/     |/-~-/ |
||    |/--+-----+------\   \+-/   |
\&gt;----~#  #     \-?#-*-+----/     |
      |1  1  /$&quot;&quot;-$#-/ |          |
      \/  |  ~---------*----------&lt;-821#-.
          \--/</pre>

##External Resources
# [https://github.com/aaronduino/asciidots Main Github repo]
# It got a writeup on Motherboard!  [https://motherboard.vice.com/en_us/article/a33dvb/asciidots-is-the-coolest-looking-programming-language]

[[Category:Languages]]
[[Category:2017]]
[[Category:Turing_complete]]
[[Category:Two-dimensional_languages]]
