# Working with Roles - Dependencies

Create (demo) roles with dependencies as following:

![](https://playpit-labs-assets.s3-eu-west-1.amazonaws.com/images/roles-dependencies.png)

Please pay attention, some roles call another one(s) with and without variables

Add following task to each role for debugging roles execution, like:

```yaml
- debug: msg="running {{ role_name }} role"
```

Please find drafts [here](dependencies/)