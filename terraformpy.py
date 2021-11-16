
"""

    This module helps in running Terraform commands using python class

"""
import os
import subprocess
import logging

class TerraformPy():
    """
        This class is the wrapper class for Terraform commands

    """
    def __init__(self, path=None) -> None:
        """Initialization method for terraformpy

        Args:
            path (string, optional): Path from where you need to run Terraform scripts.
            Defaults to current working directory.
        """
        super().__init__()
        # Create a custom logger
        self.logger = logging.getLogger(__name__)
        if path is not None:
            self.tf_path = path
        else:
            self.tf_path = os.getcwd()

    def init(self):
        """
        This method is used to run Terraform init command to download plugins

        """
        self._subprocess_cmd("terraform init -no-color 2>&1 | tee tr_out.log")

    def apply(self, **inputs):
        """This method is used to run Terraform Apply with variables

        Returns:
            string : Returns json format of the terraform output
        """
        args = " ".join({" -var "+str(k)+ "=" + "'" +str(v)+ "'" for k, v in inputs.items()})
        self._subprocess_cmd("terraform init -no-color 2>&1 | tee tr_out.log")
        self._subprocess_cmd("terraform apply -auto-approve {0} -no-color 2>&1 | \
                                tee -a tr_out.log".format(args))
        return subprocess.check_output("terraform output -json -no-color 2>&1 | \
                                tee -a tr_out.log", cwd=self.tf_path, shell=True)

    def destroy(self, **inputs):
        """
        This method is used to run Terraform Destroy with variables

        """
        args = " ".join({" -var "+str(k)+ "=" + "'" +str(v)+ "'" for k, v in inputs.items()})
        self._subprocess_cmd("terraform init -no-color 2>&1 | tee tr_out.log")
        self._subprocess_cmd("terraform destroy -auto-approve {0} -no-color 2>&1 | \
                                tee -a tr_out.log".format(args))

    def output(self, out_type="json"):
        """This method is to get the Terraform output from tf state file

        Args:
            out_type (str, optional): Terraform output type. Defaults to "json".

        Returns:
            string : Returns json format of the terraform output
        """
        return subprocess.check_output("terraform output -{0} -no-color 2>&1 | \
                                tee -a tr_out.log".format(out_type), cwd=self.tf_path, shell=True)

    def _subprocess_cmd(self, command):
        """Command processor to run Terraform commands

        Args:
            command (string): Complete Terraform command which supposed to be executed

        Raises:
            ValueError: Raises error when Terraform execution fails for any reason
        """
        self.logger.debug("Running terraform command ==> %s", command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=self.tf_path, shell=True)
        proc_stdout, proc_stderr = process.communicate()
        if (process.returncode != 0) or ('Error' in proc_stdout.decode('utf-8')):
            raise ValueError("ERROR: Terraform execution failed :"
                             + proc_stdout.decode('utf-8').strip()
                             + "/n/n" + proc_stderr.decode('utf-8').strip())
        return proc_stdout
