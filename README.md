#Jenkins Monitor deployment
## Summary
Monit is a open source monitor tool to monitor jenkins service, if any issue occurs, email notification will be sent.\

Currently, we support below monitoring
~~~
1.CPU utilization monitoring
If higher than defined cpu threadhold, email notification will be sent

2.Memory utilization monitoring
If higher than defined memory threadhold, email notification will be sent

3.Jenkins process monitoring
If process down or blocked, email will notification will be sent and monit will try to restart jenkins
~~~

##How to install Monit
yum install -y monit

##How to configure Monit
1.copy jenkins-monitor directory to /root/
2.copy jenkins.conf to /etc/monit.d/
3.pip install requests
3.run monit reload


## Configuration Steps ##
1.Create Email service in the space where buildpack manager application placed


2.Create bindable application for jenkins vmaas virtual machine 

3.bind the jenkins vmaas virtual machine bindable application to email service instance

4.Configure Email service and register email

a.configure configuration file under jenkins-monitor directory

b.run python notify register 

5.Run monit reload to reload all the configuration