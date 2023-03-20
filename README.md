# Install and usage instructions

Requires python3. Use pip to install PyPDF2, openpyxl and pandas. After that, run using the following command:
~~~
    python3 extractPDF.py [mode] [filename1] [filename2]...
~~~
The output should be called `out-[mode].xlsx`. The two options for `mode` are `trunc` (outputs a truncated spreadsheet showing only overall counts for R, PR, etc..), and a `full` spreadsheet, which shows all signals.