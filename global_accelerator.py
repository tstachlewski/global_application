import boto3

ga = boto3.client('globalaccelerator', region_name='us-west-2')

ga_arn = ga.create_accelerator( Name='GlobalApplication2', IpAddressType='IPV4', Enabled=True )["Accelerator"]["AcceleratorArn"]


listener_arn = ga.create_listener( AcceleratorArn=ga_arn, PortRanges=[ { 'FromPort': 80, 'ToPort': 80 }, ], Protocol='TCP' )["Listener"]["ListenerArn"]


lb_europe_arn = boto3.client('elbv2', region_name='eu-west-1').describe_load_balancers()["LoadBalancers"][0]["LoadBalancerArn"]
lb_usa_arn = boto3.client('elbv2', region_name='us-west-1').describe_load_balancers()["LoadBalancers"][0]["LoadBalancerArn"]


ga.create_endpoint_group(
    ListenerArn=listener_arn,
    EndpointGroupRegion='eu-west-1',
    EndpointConfigurations=[
        {
            'EndpointId': lb_europe_arn,
        },
    ],
    HealthCheckPort=80,
    HealthCheckIntervalSeconds = 10,
    HealthCheckProtocol='TCP',
    HealthCheckPath="/"
)

ga.create_endpoint_group(
    ListenerArn=listener_arn,
    EndpointGroupRegion='us-west-1',
    EndpointConfigurations=[
        {
            'EndpointId': lb_usa_arn,
        },
    ],
    HealthCheckPort=80,
    HealthCheckIntervalSeconds = 10,
    HealthCheckProtocol='TCP',
    HealthCheckPath="/"
)