import hashlib


class Message():
    def __init__(self, account_id = None, profile_id = None, contact_point = None):
        self.account_id = account_id
        self.profile_id = profile_id
        self.contact_point = contact_point

    def get_customer_id(self):
        if self.profile_id:
            customer_identifier = self.profile_id
        elif self.account_id:
            customer_identifier = self.account_id
        else:
            customer_identifier = self.contact_point
        return customer_identifier

class Test():
    def __init__(self, test_id, number_variants, weights=None):
        self.test_id = test_id
        self.number_variants = number_variants
        self.weights = weights


def which_option(message, test):
    #generate hash
    customer_identifier = message.get_customer_id()
    combined = f"{customer_identifier}{test.test_id}"
    #print("combined: "+str(combined))
    hashed = hashlib.sha224(combined.encode("utf-8")).hexdigest()
    print("last three digits:" + hashed[-3:])
    last_two = int(hashed[-3:], 16)
    print(combined+" last two: "+str(last_two)+" hashed: "+hashed)
    #add up total of variants
    variant_max = test.number_variants
    if test.weights:
        variant_max = 0
        for x in test.weights:
            variant_max += x
    variant = last_two % variant_max
    #print("variant: "+str(variant))
    if test.weights:
        total = 0
        offset = 0
        #iterate through number of variants
        for x in range(test.number_variants):
            total += test.weights[x]
            if variant < total:
                print ("variant: "+str(variant))
                print ("offset: "+str(offset))
                variant = offset
                print("variant: "+str(variant)+" offset: "+str(offset))
                break
            offset += 1
    #print(variant, customer_identifier)
    return variant, customer_identifier

if __name__ == "__main__":
     t = Test(3422, 7, weights  = [10, 10, 10, 10, 20, 20, 20])
     buckets = {}
     for x in range(100):
         m = Message(account_id=54654618+x)
         #m = Message(account_id=1+x)
         variant, customer = which_option(m, t)
         # print(variant, customer)
         if not variant in buckets:
             buckets[variant] = []
         buckets[variant].append(customer)
    
     sorted_keys = sorted(buckets.keys())
     offset = 0
     for k in sorted_keys:
         print("{:<10}".format("v{} - w{}".format(k, t.weights[offset])), end="")
         buckets[k] = sorted(buckets[k])
         offset += 1
     print()
     for k in sorted_keys:
         print(10 * "-", end="")
     print()
     offset = 0
     while True:
         printed = False
         for x in sorted_keys:
             if offset < len(buckets[x]):
                 print("{:<10}".format(buckets[x][offset]), end="")
                 printed = True
             else:
                 print(10 * " ", end="")
         if not printed:
             break
         print()
         offset += 1
     print()

     # for x in sorted(buckets.keys()):
         # print("BUCKET: ", x)
         # for y in buckets[x]:
            # print("-- ", y)