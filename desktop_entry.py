"""Native entry point with machine-readable startup diagnostics for build checks."""
import json
import os
import sys
from pathlib import Path

if __name__ == '__main__':
    # Tcl uses forward-slash paths consistently across Windows environments.
    if os.name == 'nt':
        for name in ('TCL_LIBRARY','TK_LIBRARY'):
            if name in os.environ:
                os.environ[name] = os.environ[name].replace('\\','/')
    testing = len(sys.argv) == 3 and sys.argv[1] == '--self-test'
    try:
        import app
        app.main()
    except Exception as error:
        if testing:
            resource = Path(getattr(sys,'_MEIPASS',Path(__file__).parent)) / '_tcl_data' / 'init.tcl'
            diagnostic = {'ok':False,'error':type(error).__name__ + ': ' + str(error), 'tcl_exists':resource.exists()}
            Path(sys.argv[2]).write_text(json.dumps(diagnostic),encoding='utf-8')
            raise SystemExit(1)
        raise
