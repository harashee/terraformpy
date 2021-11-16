# terraformpy
Python wrapper for Terraform

# Getting started

Initialise the terraformpy module. "tf_path" variable

```
import terraformpy
tf_client = TerraformPy()
```

Below method is used for Terraform init action

```
tf_client.init()
```

Use the below method for Terraform Apply with any number of variables.

```
tf_client.apply(var1=value1, var2=value2, ...)
```
Use the below method to get the Terraform output based on output type from tfstate file.
```
tf_client.output(out_type = "json")
```

Use the below method for Terraform Destroy with any number of variables.
```
tf_client.destroy(var1=value1, var2=value2, ...)

```
