# Quick start
The object of this tool is to extract
[lean blueprint](https://github.com/PatrickMassot/leanblueprint/)
code from a Lean file. This allows one to embed the blueprint directly into the
lean code.

To do so, include the blueprint directly as a comment in the lean file, with a
special opening and closing tag. For example:
```
/-%%
\begin{theorem}
  If $x\in\mathbb R$ and $x>0$, then $2x>0$
\end{theorem}
%%-/

theorem two_x_positive (x:ℝ) (hpos: 0<x) : 0<2*x := by
/-%%
\begin{proof}
    Multiplying both sides by $2$, which is $>0$, we find that $2x>0$.
\end{proof}
%%-/
  simp only [gt_iff_lt, zero_lt_two, zero_lt_mul_left]
  exact hpos
```

The opening and closing tags are set to `/-%%` and `%%-/` by default, but can
be customized on the command line.

In addition, the tool supports single-line blueprint code using the `--%%`
prefix: for example,
```
theorem two_x_positive (x:ℝ) (hpos: 0<x) : 0<2*x := by
--%%\begin{proof} Multiplying both sides by $2$, which is $>0$, we find that $2x>0$. \end{proof}
  simp only [gt_iff_lt, zero_lt_two, zero_lt_mul_left]
  exact hpos
```

Copying these examples to a file `test.lean`, one can extract the blueprint by
running
```
extract_blueprint `test.lean` > outfile.tex
```
In addition, the blueprint can be stripped from the file with
```
extract_blueprint -L `test.lean` > stripped.lean
```

# Usage
```
extract_blueprint [-B|-L] [-s start_delimiter] [-e end_delimiter] [-l line_delimiter] [-o output] <input_file.lean>
```

* `input_file.lean`: mandatory argument that specifies the file from which
  the blueprint is to be extracted.

* `-s <start_delimiter>` or `--start_delimiter <start_delimiter>`
  (default: `/\-%%`): a regular expression that specifies the opening tag that
  encloses blueprint code.

* `-e <end_delimiter>` or `--end_delimiter <end_delimiter>`
  (default: `/\-%%`): a regular expression that specifies the closing tag that
  encloses blueprint code.

* `-l <line_delimiter>` or `--line_delimiter <line_delimiter>`
  (default: `\-\-%%`): a regular expression that specifies the prefix for single
  line blueprint code.

* `-o <output>` or `--output <output>` (default: `stdout`): specify a file on
  which to write the output.

* `-B` or `--blueprint`: print the extracted blueprint file (this is the
  default).

* `-L` or `--lean`: print the lean code in which the blueprint has been
  removed.


# Customizing the opening and closing tags
The opening and closing tags can be specified on the command line using the
`-s` and `-e` arguments. These arguments are
[python regular expressions](https://docs.python.org/3/library/re.html).

By default, they are `/\-%%` and `%%\-/` (note the backslashes, which escape
the `-` symbol).

When customizing these, you may use any regular expression, which allows for
much flexibility. However, you must be careful to escape characters if
appropriate.

The single line prefix can be customized similarly using the `-l` argument.

# Basic examples
To extract the blueprint from a lean file `test.lean` and write it to
`blueprint.tex`:
```
extract_blueprint test.lean > blueprint.tex
```
or
```
extract_blueprint -o blueprint.tex test.lean
```

To strip the blueprint out of the lean file, use
```
extract_blueprint -L test.lean > test_stripped.lean
```

To change the opening tag to `/-blue`:
```
extract_blueprint -s '/\-blue' test.lean > blueprint.tex
```

To automatically remove spaces after the single line prefix using a regular
expression:
```
extract_blueprint -l '\-\-%% *' test.lean > blueprint.tex
```

# License
This tool is released under the GPLv3 license or later. A copy of the license
is included.

# Authors
This tool was written by Ian Jauslin and Alex Kontorovich
