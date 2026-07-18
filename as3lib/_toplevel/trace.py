from as3lib import as3state, config


def _traceFileOutput(output):
    with open(config.TraceOutputFileName, 'a') as f:
        f.write(output + '\n')


def trace(*args):
    output = ' '.join(str(i) for i in args)
    print(output)
    if config.TraceOutputFileEnable:
        _traceFileOutput(output)


def errorTrace(*args):
    output = ' '.join(str(i) for i in args)
    print(output)
    if config.ErrorReportingEnable and not as3state.MaxWarningsReached:
        if as3state.CurrentWarnings < config.MaxWarnings or config.MaxWarnings == 0:
            as3state.CurrentWarnings += 1
        else:
            output = 'Maximum number of errors has been reached. All further errors will be suppressed.'
            as3state.MaxWarningsReached = True
        _traceFileOutput(output)
