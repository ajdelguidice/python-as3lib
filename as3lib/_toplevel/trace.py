from as3lib import as3state


def trace(*args):
   if as3state.as3DebugEnable:
      output = ' '.join((str(i) for i in args))
      if as3state.TraceOutputFileEnable:
         if as3state.TraceOutputFileName.exists():
            if as3state.TraceOutputFileName.is_file():
               with open(as3state.TraceOutputFileName, 'a') as f:
                  f.write(output + '\n')
            else:
               print(output)
         else:
            with open(as3state.TraceOutputFileName, 'w') as f:
               f.write(output + '\n')
      else:
         print(output)

def errorTrace(*args):
   '''
   This is a wrapper around trace that increments as3state.CurrentWarnings 
   '''
   if as3state.ErrorReportingEnable and not as3state.MaxWarningsReached:
      if as3state.CurrentWarnings < as3state.MaxWarnings or as3state.MaxWarnings == 0:
         trace(*args)
         as3state.CurrentWarnings += 1
      else:
         trace('Maximum number of errors has been reached. All further errors will be suppressed.')
         as3state.MaxWarningsReached = True
