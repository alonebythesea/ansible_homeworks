# "base" Role

## It configures system defaults:

- installs (for example) `epel-release`, `python`, `pip`, `curl`, `wget`, `sudo`, `iproute` and other packages
- ensures that ansible facts folder exists
- discovers ansible facts (use **explicit** behaviour and gather all facts here)
- etc

It's a key role for your Roles Library

In most cases this kind of roles should be used for ensuring system is hardened:

- https://www.newnettechnologies.com/downloads/cis/Linux/CentOS/CIS_CentOS_Linux_7_Benchmark_v2.1.0.pdf


> Cloud environments and operating systems are not secure by default. Launching an image hardened according to the trusted security configuration baselines prescribed by a CIS Benchmark will reduce cost, time, and risk to an organization. This image has been hardened by CIS and is configured with the majority of the recommendations included in the free PDF version of the corresponding CIS Benchmark. The Level 1 Profile settings within the CIS Benchmark have been applied with the intent to provide a clear security benefit without inhibiting the utility of the technology beyond acceptable means.