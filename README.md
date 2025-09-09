# Azure-Cloud-Security-Monitoring-with-Sentinel-Intergration
Soc Analyst Project 

**Objectives**
- Deploy a public-facing VM in Azure
- Expose the VM to simulate real-world attack conditions
- Capture logs in Microsoft Sentinel
- Visualize attacker behavior using workbooks
- Simulate scans using nmap

**Tools used:**
1) Azure VM                                  
2) Azure Setinel                            
3) Azure Analytics
4) Network Security Groups                  
5) Nmap

**Skills learned:**
1) Kql Language
2) Azure Infrastructure
3) Network Configurations
4) Siem Intergrations
5) Log Ingestion
6) Threat Simulation and Testing
7) Threat Hunting
8) Workbook and Dashboard creation


<h2>Step 1: Project Setup</h2>
<b1>Open up a new in VM, you are able to set up a free trial or pay-as-you-go instance. If you choose pay-as-you-go keep it cheap we can use a bare bones VM and still complete our goal. In this case I went with Windows 10 Pro, smallest storage and disk that worked for Windows 10. You will notice the monthly cost of leaving the VM on 24/7. Be mindful of shutting this off when you are done. You can configure you VM to shut off at midnight daily as a saftey precaution. While in creating the VM be sure to include public IP remember the username and password created for logging into the new machine.</b1>

![image alt](https://github.com/MichaelBerry-CyberPro/Azure-Cloud-Security-Monitoring-with-Sentinel-Intergration/blob/main/new%20VM.jpeg?raw=true)

<h2>Step 2:Creating a Honey Pot (Azure Virtual Machine)</h2>
<b2>-Once the VM is created, click on the VM through the Resource Group. You will need to verify that your public IP address was created alongside with the Network Security Group. In the event is was not you can create one and this will be how the attackers find our VM across the internet. Next steps are to open up the VM to world. This is **DANGEROUS** and should only be done to test applications or projects. Delete the first default rule, and set your inbound security rules to allow all traffic from any source. </b2> 

![image alt](https://github.com/MichaelBerry-CyberPro/Azure-Cloud-Security-Monitoring-with-Sentinel-Intergration/blob/main/new%20rule%20to%20allow%20traffic.jpeg?raw=true)


This is not necessary but I want to confirm that my port 3389 was open so ran a nmap scan to confirm that they were open and able to accept outside traffic.

![image alt](https://github.com/MichaelBerry-CyberPro/Azure-Cloud-Security-Monitoring-with-Sentinel-Intergration/blob/main/Nmap%20Scan%202.png?raw=true)

![image alt](https://github.com/MichaelBerry-CyberPro/Azure-Cloud-Security-Monitoring-with-Sentinel-Intergration/blob/main/Nmap%20scan1.png?raw=true)


<b3>-Log into your VM using Remote Desktop (you will need the public IP) and you will remove all protection from the Windows Defender firewall. Again this is dangerous and should be handled with care. Open powershell on your personal computer and ping the VM Ip address to show that it can recieve data. After that log out of the Vm. Remember even though you are logged out the VM it is still running. Let it continue you to run, we need the data that will come from this.

![image alt](https://github.com/MichaelBerry-CyberPro/Azure-Cloud-Security-Monitoring-with-Sentinel-Intergration/blob/main/Ping%20ipaddress.png?raw=true) </b3>
 
<h2> Step 3: Forwarding Data</h2>
<b3>You need to create an Log Analytics Workspace and a Sentinel Instance and connect the two together. While creating these two be these are apart the the same resource group. If you cannot located these two, use the search bar at the top of Azure portal. For the sentinel instance install "Windows Security Events via AMA" Connector. You need to also create Data Collection Rules within sentinel, which fill funnel our event logs.</b3>

<h2>Step 4: Logs and Data</h2>
<b4>Log into the sentinel application and you want to drill down into your instances logs. The first query to run is Securityevents and this will be to see if you have any events populating. I personally had to let my VM run for about 3 hours before any attackers. Let it run for a while and try this query next (KQL Language):</b4> 

<b5>SecurityEvent
| where EventID == 4625
| project Account, IpAddress, EventID </b5> **(where you see the pipe that is a new line)**

EventID 4625 will populate every failed log in attempt from any user attempting to log in including the VM Owner. Down below where my results: 

![image alt](https://github.com/MichaelBerry-CyberPro/Azure-Cloud-Security-Monitoring-with-Sentinel-Intergration/blob/main/Logs%201.jpeg?raw=true)

Next we are going upload geographical data so that sentinel will create a visualization for us. Through the Setinel app we are going to create a watchlist, provide a watchlist name and upload the Geolocation csv file I have attached. This process will take some time to upload about 30mins to complete.

<h2> Step 5: Creating Attack Map Dashboard</h2>

<b5> Create a Workbook in the Sentinel app. Edit and remove the existing dashboards in place. We will run query, click on advanced editor and add the json file I have attached called map. Once you click done editing the new map will populate, be sure to save the map.
![image alt](https://github.com/MartyDickerson/Azure-Cloud-Security-Monitoring-with-Sentinel-Intergration/blob/main/images/VM_Attack_Map.png))

<h2>Project Topology</h2>

![image alt](https://github.com/MartyDickerson/Azure-Cloud-Security-Monitoring-with-Sentinel-Intergration/blob/main/images/HomeLab%20Build.png)
