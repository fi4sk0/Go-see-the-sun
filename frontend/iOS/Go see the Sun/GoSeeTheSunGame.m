//
//  GoSeeTheSunGame.m
//  Go see the Sun
//
//  Created by Timo Maul on 06.12.12.
//  Copyright (c) 2012 Timo Maul. All rights reserved.
//

#import "GoSeeTheSunGame.h"

@implementation GoSeeTheSunGame

- (NSArray*)getGames
{
    return nil;
}

- (NSString *)stringWithUrl:(NSURL *)url
{
    NSString *post = @"nickname=buhmanni&lat=5&lon=3";
    NSData *postData = [post dataUsingEncoding:NSASCIIStringEncoding                            allowLossyConversion:YES];
    
    NSString *postLength = [NSString stringWithFormat:@"%d", [postData length]];
    
	
    
    NSMutableURLRequest *request = [[NSMutableURLRequest alloc] initWithURL: url];
    [request setHTTPMethod: @"POST"];
    [request setValue:postLength forHTTPHeaderField:@"Content-Length"];
    [request setValue:@"application/x-www-form-urlencoded" forHTTPHeaderField:@"Content-Type"];
	[request setHTTPBody:postData];
    
    AFHTTPRequestOperation *myOperation = [[AFHTTPRequestOperation alloc] initWithRequest:request];
    
    [myOperation start];
    return [myOperation responseString];
    
    /*
     AFJSONRequestOperation *operation = [AFJSONRequestOperation JSONRequestOperationWithRequest:request success:^(NSURLRequest *request, NSHTTPURLResponse *response, id JSON) {
     NSLog(@"IP Address: %@", [JSON valueForKeyPath:@"origin"]);
     } failure:nil];
     
     [operation start];
     // Construct a String around the Data from the response
     return [operation responseString]; */
}

@end
