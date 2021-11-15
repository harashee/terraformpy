import subprocess
import logging

# Create a custom logger
logger = logging.getLogger(__name__)


class terraformDeployer(object):

    def apply(self, path, **inputs):
        args = " ".join({ " -var "+str(k)+ "=" + "'" +str(v)+ "'" for k,v in inputs.items()})
        self._subprocess_cmd("terraform init -no-color 2>&1 | tee tr_out.log", path = path)
        self._subprocess_cmd("terraform apply -auto-approve {0} -no-color 2>&1 | tee -a tr_out.log".format(args),path = path)
        return subprocess.check_output("terraform output -json -no-color 2>&1 | tee -a tr_out.log",cwd = path, shell=True)

    def destroy(self, path, **inputs):
        args = " ".join({ " -var "+str(k)+ "=" + "'" +str(v)+ "'" for k,v in inputs.items()})
        self._subprocess_cmd("terraform init -no-color 2>&1 | tee tr_out.log", path = path)
        self._subprocess_cmd("terraform destroy -auto-approve {0} -no-color 2>&1 | tee -a tr_out.log".format(args),path = path)

    def _subprocess_cmd(self,command,path):
        logger.debug("Running terraform command ==> {0}".format(command))
        process = subprocess.Popen(command,stdout=subprocess.PIPE,cwd=path, shell=True)
        proc_stdout,proc_stderr = process.communicate()
        if (process.returncode !=0) or ('Error' in proc_stdout.decode('utf-8') ) :
            # self.subprocess_cmd("rm {0}".format(fm_vm_name), self.terraform_base_path)
            raise ValueError("ERROR: Terraform execution failed :"+ proc_stdout.decode('utf-8').strip() )