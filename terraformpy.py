
"""

    This module helps in running Terraform commands using python class

"""
import subprocess
import logging

class TerraformPy():
    """
        This class is the wrapper class for Terraform commands

    """
    def __init__(self) -> None:
        super().__init__()
        # Create a custom logger
        self.logger = logging.getLogger(__name__)

    def init(self, path):
        """This method is used to run Terraform init command to download plugins

        Args:
            path (string): Path from where you need to run Terraform init
        """
        self._subprocess_cmd("terraform init -no-color 2>&1 | tee tr_out.log", path=path)

    def apply(self, path, **inputs):
        """This method is used to run Terraform Apply with variables

        Args:
            path (string): Path from where you need to run Terraform Apply

        Returns:
            dict: Returns json of the terraform output
        """
        args = " ".join({" -var "+str(k)+ "=" + "'" +str(v)+ "'" for k, v in inputs.items()})
        self._subprocess_cmd("terraform init -no-color 2>&1 | tee tr_out.log", path=path)
        self._subprocess_cmd("terraform apply -auto-approve {0} -no-color 2>&1 | \
                                tee -a tr_out.log".format(args), path=path)
        return subprocess.check_output("terraform output -json -no-color 2>&1 | \
                                tee -a tr_out.log", cwd=path, shell=True)

    def destroy(self, path, **inputs):
        """This method is used to run Terraform Destroy with variables

        Args:
            path (string): Path from where you need to run Terraform Destroy
        """
        args = " ".join({" -var "+str(k)+ "=" + "'" +str(v)+ "'" for k, v in inputs.items()})
        self._subprocess_cmd("terraform init -no-color 2>&1 | tee tr_out.log", path=path)
        self._subprocess_cmd("terraform destroy -auto-approve {0} -no-color 2>&1 | \
                                tee -a tr_out.log".format(args), path=path)

    def output(self, path, out_type="json"):
        """Get the terraform output from the tf state file

        Args:
            path (string): Path from where you need to run Terraform output
        """
        output = self._subprocess_cmd("terraform output -{0} -no-color 2>&1"
                                      .format(out_type), path=path)
        return output

    def _subprocess_cmd(self, command, path):
        """Command processor to run Terraform commands

        Args:
            command (string): Complete Terraform command which supposed to be executed
            path (string): Path from where you need to run Terraform scripts

        Raises:
            ValueError: Raises error when Terraform execution fails for any reason
        """
        self.logger.debug("Running terraform command ==> %s", command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=path, shell=True)
        proc_stdout, proc_stderr = process.communicate()
        if (process.returncode != 0) or ('Error' in proc_stdout.decode('utf-8')):
            raise ValueError("ERROR: Terraform execution failed :"
                             + proc_stdout.decode('utf-8').strip()
                             + "/n/n" + proc_stderr.decode('utf-8').strip())
        return proc_stdout
