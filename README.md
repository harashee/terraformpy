# terraformpy
Python wrapper for Terraform

# Example usage

```
import terraformpy
tf_path = "~/."
tf_client = TerraformPy()

tf_client.init(tf_path)

tf_client.apply(tf_path, var1=value1, var2=value2, ...)

tf_client.destroy(tf_path, var1=value1, var2=value2, ...)

```
