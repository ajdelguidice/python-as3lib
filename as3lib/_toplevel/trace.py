from as3lib import as3state


def trace(*args, isError=False):
   if as3state.as3DebugEnable:
      if isError == True and as3state.ErrorReportingEnable:
         if as3state.MaxWarningsReached:
            pass
         if as3state.CurrentWarnings < as3state.MaxWarnings or as3state.MaxWarnings == 0:
            output = ' '.join(args)
            as3state.CurrentWarnings += 1
         else:
            output = "Maximum number of errors has been reached. All further errors will be suppressed."
            as3state.MaxWarningsReached = True
      else:
         output = ' '.join((str(i) for i in args))
      if as3state.TraceOutputFileEnable:
         if as3state.TraceOutputFileName.exists():
            if as3state.TraceOutputFileName.is_file():
               with open(as3state.TraceOutputFileName, "a") as f:
                  f.write(output + "\n")
            else:
               print(output)
         else:
            with open(as3state.TraceOutputFileName, "w") as f:
               f.write(output + "\n")
      else:
         print(output)
