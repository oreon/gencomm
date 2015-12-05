from django.db import models


class Person(models.Model): 

               gender = models.  firstName = models.CharField(max_length=30,null = False, blank = True)
        
               dob = models.DateField(null = False, blank = True)
        
               class Meta:
                    abstract = True
    

class Department(models.Model): 
            
               name = models.  firstName = models.CharField(max_length=30,null = False, blank = True)

# Create your models here.
class Employee(Person): 

            # @ManyToOne(targetEntity="Employee", inversedBy="employees")
               department = models.ForeignKey(Department, related_name='employees')
            
        
               firstName = models.  firstName = models.CharField(max_length=30,null = False, blank = True)
        
               lastName = models.  firstName = models.CharField(max_length=30,null = False, blank = True)
        
    


 
class Customer(Person): 

               firstName = models.  firstName = models.CharField(max_length=30,null = False, blank = True)
        
               lastName = models.  firstName = models.CharField(max_length=30,null = False, blank = True)
        
                
            

 
class CustomerOrder(models.Model): 

               notes = models.TextField(null = False, blank = True)
        
            # @ManyToOne(targetEntity="CustomerOrder", inversedBy="customerOrder")
               customer = models.ForeignKey(Customer, related_name='customerOrder')
                        
        
               shipDate = models.DateField(null = False, blank = True)
        
            # @ManyToOne(targetEntity="CustomerOrder", inversedBy="customerOrder")
             #  paymentMethod = models.ForeignKey(PaymentMethod, related_name='customerOrder')
        
    
    


 
class Product(models.Model): 

               name = models.  firstName = models.CharField(max_length=30,null = False, blank = True)
        
    



 
class OrderItem(models.Model): 

               qty = models. IntegerField(null = False, blank = True)
        
            # @ManyToOne(targetEntity="OrderItem", inversedBy="orderItem")
               product = models.ForeignKey(Product, related_name='orderItem')
            
        
            # @ManyToOne(targetEntity="OrderItem", inversedBy="orderItems")
               customerOrder = models.ForeignKey(CustomerOrder, related_name='orderItems')
            
        
    
    
    
    


 
