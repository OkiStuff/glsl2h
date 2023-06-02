import typing as t
import sys
import timeit
from pathlib import Path

__VERSION__: str = "v1.0.0"

def message(msg: str) -> None:
    print(f"glsl2h: {msg}")

def error(msg: str) -> None:
    message(f"error: {msg}")

def debug(msg: str) -> None:
    message(f"debug: {msg}")

def info(msg: str) -> None:
    message(f"info: {msg}") 

def main() -> None:
    if (len(sys.argv) < 4):
        error(f"expected 3 arguments, got {len(sys.argv) - 1}")
        error("syntax: glsl2h.py [fileIn] [fileOut] [macroName]")
        return
        
    info(f"version {__VERSION__} GPL v2.0 License")
    
    start_time: float = timeit.timeit()
    infile: Path = Path(sys.argv[1])
    outfile: Path = Path(sys.argv[2])
    macro_name: str = sys.argv[3].upper()
    
    infile_exists: bool = infile.exists() and infile.is_file()
    outfile_exists: bool = outfile.exists() and outfile.is_file()
    
    debug(f"fileIn={infile}; exists={infile_exists}{'; error here' if not infile_exists else ''}")
    debug(f"fileOut={outfile}; exists={outfile_exists}")
    debug(f"macroName={macro_name}")
    
    if (not infile_exists):
        error("quitting... view debug statements above for details")
        return
    
    infile_contents: str = str()
    
    with open(str(infile), "r") as f:
        debug(f"reading {infile}")    
        infile_contents = f.read()
        debug(f"read; closing {infile}...")
    
    outfile_contents: str = f"""#ifndef {macro_name}_H
#define {macro_name}_H
// Generated using glsl2h

#define {macro_name} \\
"""

    line: int = 0
    linebuffer: str = str()
    for char in infile_contents:
        if (char == "\n"):
            line += 1
            outfile_contents += f'"{linebuffer}\\n" \\\n' if char != infile_contents[-1] else f'"{linebuffer}\\n\\0" \n'
            linebuffer = str()
            continue
        
        linebuffer += char
    
    outfile_contents += f"#endif //{macro_name}_H"
    debug("completed transforming data")
    
    with open(str(outfile), "w") as f:
        debug(f"writing to {outfile}")
        f.write(outfile_contents)
        debug(f"write done; closing {outfile}")
    
    info(f"{infile} to {outfile} completed in {round(start_time - timeit.timeit())}s")
    

if (__name__ == "__main__"):
    main()