
from io import StringIO

from IPython.kernel.zmq.kernelbase import Kernel
from IPython.display import HTML

a = '<p style="font-size:20px;background-color:black;color:yellow;">&gt;&gt;&gt;&nbsp;'
b = '</p>'

class PrintKernel(Kernel):
    implementation = 'Print'
    implementation_version = '-31.0'
    language = 'no-op'  # will be used for
                        # syntax highlighting
    language_version = ''
    banner = "Advanced printing in the notebook"
    
    def do_execute(self, code, silent,
                   store_history=True,
                   user_expressions=None,
                   allow_stdin=False):

        expr = None
        try:
            expr = code.split('print(')[1].split(')')[0]
            out = HTML(a + str(eval(expr)) + b)
        except:
            pass

        if not code.strip():
            return {'status': 'ok', 
                    'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}
        
        if not silent:
            if expr:
                # We send the standard output to the client.
                self.send_response(self.iopub_socket,
                    'stream', {
                        'name': 'stdout', 
                        'data': 'Richer print'})

                # We prepare the response with our rich data
                # (the plot).
                content = {'source': 'kernel',
                           'data': {'text/html': out.data},
                           'metadata': {},
                           'text': [repr(out)]}        

                # We send the display_data message with the
                # contents.
                self.send_response(self.iopub_socket,
                    'display_data', content)
            
            else:
                stream_content = {'name': 'stdout', 'data': output}
                self.send_response(self.iopub_socket, 
                                   'stream', stream_content)

        # We return the exection results.
        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {}}

if __name__ == '__main__':
    from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=PrintKernel)
