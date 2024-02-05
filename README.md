# Quick start
`extract_blueprint` is a tool to extract
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

In addition, `extract_blueprint` supports single-line blueprint code using the
`--%%` prefix: for example,
```
theorem two_x_positive (x:ℝ) (hpos: 0<x) : 0<2*x := by
--%%\begin{proof} Multiplying both sides by $2$, which is $>0$, we find that $2x>0$. \end{proof}
  simp only [gt_iff_lt, zero_lt_two, zero_lt_mul_left]
  exact hpos
```
(Note that, when using the single-line code, extra newlines are added. If one
is in a math environment, this can break the LaTeX compilation process. To
avoid this, use `%nobreak%`, as explained below in section
[nobreak](#nobreak).)

Copying these examples to a file `test.lean`, one can extract the blueprint by
running
```
extract_blueprint test.lean > outfile.tex
```
In addition, the blueprint can be stripped from the file with
```
extract_blueprint -L test.lean > stripped.lean
```

One can specify multiple input files, in which case the blueprint is extracted
from each file. By default, the output is a concatenation of all blueprints to
stdout. Alternatively, one can specify a directory with the `-O` argument, in
which case the blueprint for each input file will be written in its own file.
For example:
```
extract_blueprint -O blueprint test1.lean test2.lean
```
will write the blueprint to `blueprint/test1.tex` and `blueprint/test2.tex`.

# Usage
```
extract_blueprint [-B|-L] [-f] [-s start_delimiter] [-e end_delimiter] [-l line_delimiter] [-O output_dir] <input_file1.lean> ...
```

* `input_file1.lean` `...`: one or more files from which the blueprint is to be
  extracted.

* `-s <start_delimiter>` or `--start_delimiter <start_delimiter>`
  (default: `/\-%%`): a regular expression that specifies the opening tag that
  encloses blueprint code.

* `-e <end_delimiter>` or `--end_delimiter <end_delimiter>`
  (default: `\-%%/`): a regular expression that specifies the closing tag that
  encloses blueprint code.

* `-l <line_delimiter>` or `--line_delimiter <line_delimiter>`
  (default: `\-\-%%`): a regular expression that specifies the prefix for single
  line blueprint code.

* `-O <output_dir>` or `--outdir <output_dir>`: specify a directory to which
  the output is to be written. `extract_blueprint` will generate one output
  file per input file. If run with the `-B` option, the `.lean` extension is
  replaced with `.tex`. Otherwise, the output file name is the same as the
  input file name.  `<output_dir>` must exist.

* `-B` or `--blueprint`: print the extracted blueprint file (this is the
  default).

* `-L` or `--lean`: print the lean code in which the blueprint has been
  removed.

* `-f` or `--force`: by default, if an output file would overwrite an input
  file, the program exits. Use `-f` to enable overwriting input files.

# nobreak
`extract_blueprint` automatically adds blank lines in between blueprint blocks,
which is a more natural way to parse paragraphs. However, this can cause issues
inside math modes: LaTeX does not allow blank lines in math mode. To prevent
this, one can use the %nobreak% tag, which will prevent `extract_blueprint`
from adding new lines at that location.

For example, to typeset
```
\begin{equation}
\psi=3,
\phi=4
\end{equation}
```
if one were to use
```
--%%\begin{equation}
--%%\psi=3,
--%%\phi=4
--%%\end{equation}
```
then the output would be
```
\begin{equation}

\psi=3,

\phi=4

\end{equation}
```
and would fail to compile. Instead, use
```
--%%\begin{equation}%nobreak%
--%%\psi=3,%nobreak%
--%%\phi=4%nobreak%
--%%\end{equation}
```

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

To strip the blueprint out of the lean file, use
```
extract_blueprint -L test.lean > test_stripped.lean
```

To extract the blueprints out of all of the lean files in a project and write
them to `blueprint`:
```
extract_blueprint -O blueprint ProjectName/*.lean
```
where `ProjectName` should be replaced with the name of your project.
Alternatively, you can scrape all lean files in subdirectories:
```
extract_blueprint -O blueprint **/*.lean
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
`extract_blueprint` is released under the GPLv3 license or later. A copy of the
license is included.

# Authors
`extract_blueprint` was written by Ian Jauslin and Alex Kontorovich
