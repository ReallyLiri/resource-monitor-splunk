# Resource Monitoring Service

This docker image is used to monitor availability of resources using periodical uptime checks.

## Configuration

The monitored resources are defined in `config.json`. Configurable properties:

* `splunk_url`: The address of your splunk server collector endpoint. i.e `https://splunk:8088/services/collector`
* `splunk_token`: Your splunk HEC token.
* `address`: The public address under which your resources are deployed. For multiple addresses you'd need to extend the configuration to your needs.
* `subdomains`: Which subdomains are of interest under `address`.
* `paths`: URI paths to query, by their display name.

## Build

`docker build -t resource-monitor-splunk .`

## Deployment

To run:

`docker run -d --name resource-monitor-splunk resource-monitor-splunk`

The image can also be easily deployed to your Kubernetes cluster, just make sure to set the image name in the yaml:

`kubectl apply -f resource-monitor-splunk.yaml`

## Monitoring

On any availability check (successful or not), a splunk log is generated.

Using splunk alerts we can notify on resources that are not available.

Successful log example:

```
host = Monitoring-Service
source = the-backend-in-staging-env
sourcetype = json
{  
	"code":200,
	"downtime_min":0,
	"message":"success",
	"name":"The backend in staging env",
	"url":"https://staging.domain.com/api"
}
```

Error log example:

```
host = Monitoring-Service
source = the-backend-in-staging-env
sourcetype = json
{  
	"code":404,
	"downtime_min":11285,
	"message":"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\">\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>\n",
	"name":"The backend in staging env",
	"url":"https://staging.domain.com/api"
}
```
