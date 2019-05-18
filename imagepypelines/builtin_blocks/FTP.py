import ftplib
import io
from .. import BatchBlock


class FTP(BatchBlock):
    def __init__(self, host, user, passwd, remote_cwd=None, tls=True, timeout=30):
        io_kernel = {io.IOBase : str}

        if tls:
            self.session = ftplib.FTP_TLS(host, user, passwd, timeout=30)
            self.session.login()
            self.session.prot_p()
        else:
            self.session = ftplib.FTP(host, user, passwd, timeout=30)
            self.session.login()

        if not remote_cwd:
            self.session.cwd(remote_cwd)


        super().__init__(io_kernel,
                        requires_training=False,
                        requires_labels=False)



    def process(self, datum):
        try:
            self.session.storbinary("STOR " + self.name, xdatum)
        except ftplib.all_errors:
            return False

        return True

    def __del__(self):
        if hasattr(self,'session'):
            self.session.quit()