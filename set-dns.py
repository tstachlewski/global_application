import boto3

lb_europe = boto3.client('elbv2', region_name='eu-west-1').describe_load_balancers()["LoadBalancers"][0]["DNSName"];
boto3.client('route53').change_resource_record_sets( HostedZoneId='Z008009673PAB8NPTCK0', ChangeBatch={ 'Changes': [ { 'Action': 'CREATE', 'ResourceRecordSet': { 'Name': 'europe.underthe.cloud', 'Type': 'A', 'Weight' : 1, 'SetIdentifier': 'europe', 'AliasTarget': { 'HostedZoneId': 'Z32O12XQLNTSW2', 'DNSName': lb_europe, 'EvaluateTargetHealth': False } } }, ] } )

lb_usa = boto3.client('elbv2', region_name='us-west-1').describe_load_balancers()["LoadBalancers"][0]["DNSName"];
boto3.client('route53').change_resource_record_sets( HostedZoneId='Z008009673PAB8NPTCK0', ChangeBatch={ 'Changes': [ { 'Action': 'CREATE', 'ResourceRecordSet': { 'Name': 'usa.underthe.cloud', 'Type': 'A', 'Weight' : 1, 'SetIdentifier': 'usa',  'AliasTarget': { 'HostedZoneId': 'Z368ELLRRE2KJ0', 'DNSName': lb_usa, 'EvaluateTargetHealth': False } } }, ] } )

boto3.client('route53').change_resource_record_sets( ChangeBatch={ 'Changes': [ { 'Action': 'CREATE', 'ResourceRecordSet': { 'AliasTarget': { 'DNSName': lb_europe, 'EvaluateTargetHealth': True, 'HostedZoneId': 'Z32O12XQLNTSW2', }, 'Region': 'eu-west-1', 'Name': 'dns.underthe.cloud', 'SetIdentifier': 'europe', 'Type': 'A', }, }, { 'Action': 'CREATE', 'ResourceRecordSet': { 'AliasTarget': { 'DNSName': lb_usa, 'EvaluateTargetHealth': True, 'HostedZoneId': 'Z368ELLRRE2KJ0', }, 'Region': 'us-west-2', 'Name': 'dns.underthe.cloud', 'SetIdentifier': 'usa', 'Type': 'A', }, }, ] }, HostedZoneId='Z008009673PAB8NPTCK0', )