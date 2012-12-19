//
//  ViewController.h
//  Go see the Sun
//
//  Created by Timo Maul on 05.12.12.
//  Copyright (c) 2012 Timo Maul. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "AFJSONRequestOperation.h"

@interface ViewController : UIViewController

@property (weak, nonatomic) IBOutlet UITextField *latField;
@property (weak, nonatomic) IBOutlet UITextField *lonField;
@property (weak, nonatomic) IBOutlet UITextField *addressField;

- (IBAction)sendButton:(id)sender;

@end
