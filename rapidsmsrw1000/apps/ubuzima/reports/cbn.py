####SAMPLE MESSAGE #####
##res_EN = "The correct format message is: CBN MOTHER_ID CHILD_NUM DOB CHILD_HEIGHT CHILD_WEIGHT"
##res_FR = "Andika: CBN INDANGAMUNTU NUMERO_Y_UMWANA ITARIKI_YAVUTSE IBUBUREBURE UBUREMERE"
##msg = "CBN 1198156435491265 01 13.02.2011 HT40.5 WT4.1"
###m = re.search("cbn\s+(\d+)\s+([0-9]+)\s([0-9.]+)\s(ht\d+\.?\d)\s(wt\d+\.?\d)\s?(.*)", msg, re.IGNORECASE)   
###groups = ('1198156435491265', '01', '13.02.2011', 'HT40.5', 'WT4.1', '')
#        nid = m.group(1)
#        number = m.group(2)
#        chidob = m.group(3)
#        height = m.group(4)
#        weight = m.group(5)

    #CBN keyword
    @keyword("\s*cbn(.*)")
    def cbn(self, message, notice):
        """CBN report.  """
        
        if not getattr(message, 'reporter', None):
            message.respond(_("You need to be registered first, use the REG keyword"))
            return True
            
        m = re.search("cbn\s+(\d+)\s+([0-9]+)\s([0-9.]+)\s(ht\d+\.?\d)\s(wt\d+\.?\d)\s?(.*)", message.text, re.IGNORECASE)
        if not m:
            message.respond(_("The correct format message is: CBN MOTHER_ID CHILD_NUM DOB CHILD_HEIGHT CHILD_WEIGHT"))
            return True

        nid = m.group(1)
        number = m.group(2)
        chidob = m.group(3)
        height = m.group(4)
        weight = m.group(5)

        # get or create the patient
        patient = self.get_or_create_patient(message.reporter, nid)
        
        report = self.create_report('Case Based Nutrition', patient, message.reporter)
        
        # read our fields
        try:
            (fields, dob) = self.read_fields("", False, False)
    	    dob = self.parse_dob(chidob)
        except Exception, e:
            # there were invalid fields, respond and exit
            message.respond("%s" % e)
            return True

        # set the dob for the child if we got one
        if dob:
            report.set_date_string(dob)
            
        # set the child number
        child_num_type = FieldType.objects.get(key='child_number')
        fields.append(Field(type=child_num_type, value=Decimal(str(number))))

        # save the report
        report.save()
                
        # then associate all our fields with it
        fields.append(self.read_weight(weight, weight_is_mothers=False))
        fields.append(self.read_height(height, height_is_mothers=False))

        for field in fields:
            field.save()
            report.fields.add(field)            
        
        # either send back the advice text or our default msg
        try:	response = self.run_triggers(message, report)
        except:	response = None
        if response:
            message.respond(response)
        else:
            message.respond(_("Thank you! CBN report submitted successfully."))
            
        # cc the supervisor if there is one
        try:	self.cc_supervisor(message, report)
   	except:	pass  
    	        
        return True
    
        #CBN keyword

