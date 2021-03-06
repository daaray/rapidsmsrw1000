#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django.db import models
from django.contrib.auth.models import *
from rapidsms.models import *
from rapidsms.contrib.messagelog.models import Message
from django.db.models.signals import post_save
import datetime
# Create your Django models here, if you need them.


class Role(models.Model):
    """Basic representation of a role that someone can have.  For example,
    'supervisor' or 'data entry clerk'"""
    name = models.CharField(max_length=160, unique = True)
    code = models.CharField(max_length=20, unique = True, blank=True, null=True,\
    help_text="Abbreviation")

    class Meta:
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
        ("can_view", "Can view"),
        )

    def __unicode__(self):  return self.name

class Nation(models.Model):
    """Country....the maximum code is ten because of the last low level of ISO is village which usually has ten characters"""
    name = models.CharField(max_length=160)
    code = models.CharField(max_length=10, unique = True, blank=True, null=True,\
        			help_text="Country Own code in ISO Coding SYSTEM.....For Rwanda the code is 00. because the province are 01, 02, 03, 04, then 05")

    class Meta:
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
        ("can_view", "Can view"),
        )

    def __unicode__(self):  return self.name

class Province(models.Model):
    """Province....the maximum code is ten because of the last low level of ISO is village which usually has ten characters"""
    name 	= models.CharField(max_length=160)
    code 	= models.CharField(max_length=10, unique = True,  blank=True, null=True,\
				    help_text="Province Own code in ISO Coding SYSTEM....")
    nation 	= models.ForeignKey(Nation, related_name="province_nation", null=True, blank=True, help_text=" The country the province is from")

    class Meta:
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
        ("can_view", "Can view"),
        ) 

    def __unicode__(self):  return self.name

class District(models.Model):
    """District....the maximum code is ten because of the last low level of ISO is village which usually has ten characters"""
    name 	 = models.CharField(max_length=160)
    code 	 = models.CharField(max_length=10, unique = True,  blank=True, null=True,\
				    help_text="District Own code in  ISO Coding SYSTEM .....")
    nation 	 = models.ForeignKey(Nation, related_name="district_nation", null=True, blank=True, help_text=" The country the district is from") 
    province = models.ForeignKey(Province, related_name="ditrict_province", null=True, blank=True, help_text=" The province the district is from")

    class Meta:
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
        ("can_view", "Can view"),
        )    

    def __unicode__(self):  return self.name

class Sector(models.Model):
    """Sector....the maximum code is ten because of the last low level of ISO is village which usually has ten characters"""
    name 	 = models.CharField(max_length=160)
    code 	 = models.CharField(max_length=10, unique = True,  blank=True, null=True,\
				    help_text="Sector Own code in  ISO Coding SYSTEM .....")
    nation 	 = models.ForeignKey(Nation, related_name="sector_nation", null=True, blank=True, help_text=" The country the sector is from") 
    province = models.ForeignKey(Province, related_name="sector_province", null=True, blank=True, help_text=" The province the sector is from")
    district		= models.ForeignKey(District, related_name="sector_district", null=True, blank=True, help_text=" The district the sector is from")

    class Meta:
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
        ("can_view", "Can view"),
        )

    def __unicode__(self):  return self.name

class Cell(models.Model):
    """Cell....the maximum code is ten because of the last low level of ISO is village which usually has ten characters"""
    name 	 = models.CharField(max_length=160)
    code 	 = models.CharField(max_length=10, unique = True,  blank=True, null=True,\
				    help_text="Cell Own code in  ISO Coding SYSTEM .....")
    nation 	 = models.ForeignKey(Nation, related_name="cell_nation", null=True, blank=True, help_text=" The country the cell is from") 
    province = models.ForeignKey(Province, related_name="cell_province", null=True, blank=True, help_text=" The province the cell is from")
    district		= models.ForeignKey(District, related_name="cell_district", null=True, blank=True, help_text=" The cell the cell is from")
    sector			= models.ForeignKey(Sector, related_name="cell_sector", null=True, blank=True, help_text=" The sector the cell is from")

    class Meta:
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
        ("can_view", "Can view"),
        )

    def __unicode__(self):  return self.name

class Village(models.Model):
    """Village....the maximum code is ten because of the last low level of ISO is village which usually has ten characters"""
    name 	 = models.CharField(max_length=160)
    code 	 = models.CharField(max_length=10, unique = True,  blank=True, null=True,\
				    help_text="Village Own code in  ISO Coding SYSTEM .....")
    nation 	 = models.ForeignKey(Nation, related_name="village_nation", null=True, blank=True, help_text=" The country the village is from") 
    province = models.ForeignKey(Province, related_name="village_province", null=True, blank=True, help_text=" The province the village is from")
    district		= models.ForeignKey(District, related_name="village_district", null=True, blank=True, help_text=" The cell the village is from")
    sector			= models.ForeignKey(Sector, related_name="village_sector", null=True, blank=True, help_text=" The sector the village is from")
    cell			= models.ForeignKey(Cell, related_name="village_cell", null=True, blank=True, help_text=" The cell the village is from")

    class Meta:
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
        ("can_view", "Can view"),
        )

    def __unicode__(self):  return self.name

    @classmethod
    def get_village(cls, name, cell = None, sector = None, district = None):
        try:
            if cell:
                village = Village.objects.filter(name__icontains = name, cell = cell)
                return village[0]
            elif sector:
                village = Village.objects.filter(name__icontains = name, sector = sector)
                return village[0]
            elif district:
                village = Village.objects.filter(name__icontains = name, district = district)
                return village[0]
            else:   return None         
        except:
            return None


class Hospital(models.Model):
    """Hospital....the maximum code is ten because of the last low level of ISO is village which usually has ten characters"""
    name 	 = models.CharField(max_length=160)
    code 	 = models.CharField(max_length=10, unique = True,  blank=True, null=True,\
				    help_text="Hospital Own code in  FOSA Coding SYSTEM .....")
    nation 	 = models.ForeignKey(Nation, related_name="hospital_nation", null=True, blank=True, help_text=" The country the hospital is from") 
    province = models.ForeignKey(Province, related_name="hospital_province", null=True, blank=True, help_text=" The province the hospital is from")
    district		= models.ForeignKey(District, related_name="hospital_district", null=True, blank=True, help_text=" The district the hospital is from")
    sector			= models.ForeignKey(Sector, related_name="hospital_sector", null=True, blank=True, help_text=" The sector the hospital is from")

    class Meta:
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
        ("can_view", "Can view"),
        )

    def __unicode__(self):  return self.name

class HealthCentre(models.Model):
    """Health Centre....the maximum code is ten because of the last low level of ISO is village which usually has ten characters"""
    name 	 = models.CharField(max_length=160)
    code 	 = models.CharField(max_length=10, unique = True,  blank=True, null=True,\
				    help_text="Health Centre Own code in  FOSA Coding SYSTEM .....")
    nation 	 = models.ForeignKey(Nation, related_name="hc_nation", null=True, blank=True, help_text=" The country the health centre is from") 
    province = models.ForeignKey(Province, related_name="hc_province", null=True, blank=True, help_text=" The province the health centre is from")
    district		= models.ForeignKey(District, related_name="hc_district", null=True, blank=True, help_text=" The district the health centre is from")
    sector			= models.ForeignKey(Sector, related_name="hc_sector", null=True, blank=True, help_text=" The sector the health centre is from")

    class Meta:
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
        ("can_view", "Can view"),
        )

    def __unicode__(self):  return self.name
	


class Reporter(models.Model):
    """This model represents a KNOWN person, that can be identified via
    their alias and/or connection(s). Unlike the RapidSMS Person class,
    it should not be used to represent unknown reporters, since that
    could lead to multiple objects for the same "person". Usually, this
    model should be created through the WebUI, in advance of the reporter
    using the system - but there are always exceptions to these rules..."""

    education_primaire 	= 'P'
    education_secondaire 	= 'S'
    education_universite	= 'U'
    education_ntayo 	= 'N'
    sex_female		= 'F'
    sex_male		= 'M'
    language_english	= 'en'
    language_french		= 'fr'
    language_kinyarwanda	= 'rw'


    SEX_CHOICES		= ( (sex_female, "Female"),
            		(sex_male, "Male"))

    LANGUAGE_CHOICES = ( (language_english, "English"),
            (language_french, "French"),
            (language_kinyarwanda, "Kinyarwanda"))


    EDUCATION_CHOICES = ( (education_primaire, "Primary"),
            (education_secondaire, "Secondary"),
            (education_universite, "University"),
            (education_ntayo, "None"))

    surname         	= models.CharField(max_length=50, blank=True, null = True, help_text="Family name please")
    given_name      	= models.CharField(max_length=50, blank=True, null = True, help_text="Other names")
    role            	= models.ForeignKey(Role, related_name="role", null=True, blank=True, help_text="The role you play in the community")
    sex 	        	= models.CharField(max_length = 1, blank=True, null = True, choices= SEX_CHOICES, help_text="Select the gender or sex")
    education_level 	= models.CharField(max_length = 1, blank=True, null = True, choices= EDUCATION_CHOICES, help_text="Select Education Level")
    date_of_birth		= models.DateField(blank=True, null = True, help_text="Your Date Of Birth, if date not known just pick First January")
    join_date		= models.DateField(blank=True, null = True, help_text="The date you joined the Community Health Worker program")
    national_id		= models.CharField(max_length=16, unique = True, help_text="The National ID as a sixteen digit please")
    telephone_moh		= models.CharField(max_length=13, unique = True, help_text="The telephone number only the one provided by Ministry of Health")
    village			= models.ForeignKey(Village, related_name="chw_village", null=True, blank=True, help_text=" The village you live in")
    cell			= models.ForeignKey(Cell, related_name="chw_cell", null=True, blank=True, help_text=" The cell you live in")
    sector			= models.ForeignKey(Sector, related_name="chw_sector", null=True, blank=True, help_text=" The sector you live in")
    health_centre		= models.ForeignKey(HealthCentre, related_name="chw_hc", null=True, blank=True, help_text=" The health centre you report to ")
    referral_hospital	= models.ForeignKey(Hospital, related_name="chw_hospital", null=True, blank=True, 
						        help_text=" The referral hospital of the health centre you report to")
    district		= models.ForeignKey(District, related_name="chw_district", null=True, blank=True, help_text=" The district you live in")
    province		= models.ForeignKey(Province, related_name="chw_province", null=True, blank=True, help_text=" The province you live in")
    nation			= models.ForeignKey(Nation, related_name="chw_nation", null=True, blank=True, help_text=" The country you live in")
    created			= models.DateTimeField(auto_now_add = True, blank=True, null = True, help_text="The date you are registered in the RapidSMS System")
    updated			= models.DateTimeField(blank=True, null = True, help_text="The date of last modification about the current details of CHW")

    language = models.CharField(max_length = 2, blank=True, null = True, choices= LANGUAGE_CHOICES, help_text="Select the preferred language to receive SMS")
    deactivated = models.BooleanField(default=False, help_text="Deactivate Reporter Telephone Number when is no longer used.")

    class Meta:
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
        ("can_view", "Can view"),
        )

    def __unicode__(self):
        return self.telephone_moh

    def full_name(self):
        return ("%s %s" % (
                self.given_name,
                self.surname)).strip()

    def get_connections(self):
        connections = None
        
        try:
            contact, created = Contact.objects.get_or_create(name = self.national_id)
            if self.language:    contact.language = self.language.lower()
            else:   contact.language = 'rw'

            backends = Backend.objects.all()
            for b in backends:
                try:
                    identity = self.telephone_moh if b.name != 'message_tester' else self.telephone_moh.replace('+','')
                    connection, created = Connection.objects.get_or_create(contact = contact, backend = b, identity = identity)
                    connection.save()
                except Exception,e:
                    continue
            
            contact.save()
            connections = Connection.objects.filter(contact = contact)
        except Exception, e:
            pass
            
        return connections

    def last_seen(self):
        """Returns the Python datetime that this Reporter was last seen,
            on any Connection. Before displaying in the WebUI, the output
           should be run through the XXX  filter, to make it prettier."""
        
        # comprehend a list of datetimes that this
        # reporter was last seen on each connection,
        # excluding those that have never seen them
        timedates = [
                        c.date
                        for c in Message.objects.filter( connection__in = Connection.objects.filter(contact__name = self.national_id))
                        if c.date is not None]
        
        # return the latest, or none, if they've
        # has never been seen on ANY connection
        return max(timedates) if timedates else None

    def connection(self):
        """Returns the connection object last used by this Reporter.
        The field is (probably) updated by app.py when receiving
        a message, so depends on _incoming_ messages only."""
        
        # TODO: add a "preferred" flag to connection, which then
        # overrides the last_seen connection as the default, here
        try:
            return Connection.objects.get(contact__name = self.national_id, contact = self.contact())#Connection.objects.get(contact__name = self.national_id, pk = Message.objects.filter( date = self.last_seen(), contact = self.contact())[0].connection.id)
        
        # if no connections exist for this reporter (how
        # did that happen?!), then just return None...
        except Connection.DoesNotExist:
            return None

    def contact(self):
        """Returns the connection object last used by this Reporter.
        The field is (probably) updated by app.py when receiving
        a message, so depends on _incoming_ messages only."""
        
        # TODO: add a "preferred" flag to connection, which then
        # overrides the last_seen connection as the default, here
        try:
            return Contact.objects.get(name = self.national_id)
        
        # if no connections exist for this reporter (how
        # did that happen?!), then just return None...
        except Contact.DoesNotExist:
            return None

    #Supervisors! This function avoid fetching everywhere supervisors of a reporter.
    def reporter_sups(self):
        sups = Supervisor.objects.filter(health_centre = self.health_centre)
        return sups

    def reporter_district_sups(self):
        sups = Supervisor.objects.filter(referral_hospital = self.referral_hospital)
        return sups 
    #End of Supervisors!

    
    #Expired reporter 
    def is_expired(self):
        if not self.last_seen() or self.last_seen().date() < datetime.date.today()-datetime.timedelta(30):
            return True
        return False


class RegistrationConfirmation(models.Model):
    """This allow from those CHW we registered who have confirmed that are CHWs and who are not.
	    Two days after we need to clone a reminder to ask registered CHWs to respond if they have not yet.
	    We also need to print out a list of CHWs who have not responded after five days."""
    reporter  = models.ForeignKey(Reporter, related_name="chw", unique = True, help_text=" The reporter we sent a registration confirmation")
    sent	  = models.DateField(blank=True, null = True, help_text="The date RapidSMS sent the registration request")
    received  = models.DateField(blank=True, null = True, help_text="The date RapidSMS received the registration response from the CHWs")
    responded = models.BooleanField(default=False, help_text="Did the CHW responded?")
    answer	  = models.BooleanField(default=False, help_text="The answer from CHW")

    class Meta:
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
        ("can_view", "Can view"),
        )

    def __unicode__(self):
        return "%s : %s" % (self.reporter.telephone_moh, self.answer)

def fosa_to_code(fosa_id):
    """Given a fosa id, returns a location code"""
    return "F" + fosa_id

def code_to_fosa(code):
    """Given a location code, returns the fosa id"""
    return code[1:]

class Error(models.Model):
    row = models.CharField(max_length = 10)
    sheet = models.CharField(max_length = 50)
    upload_ref = models.CharField(max_length = 50)
    district = models.ForeignKey(District)
    when	 = models.DateTimeField()	
    by	 = models.ForeignKey(User)
    error_message = models.CharField(max_length = 300)

    class Meta:
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
        ("can_view", "Can view"),
        )

    def __unicode__(self):
        return self.row

class Warn(models.Model):
    row = models.CharField(max_length = 10)
    sheet = models.CharField(max_length = 50)
    upload_ref = models.CharField(max_length = 50)
    district = models.ForeignKey(District)
    when	 = models.DateTimeField()	
    by	 = models.ForeignKey(User)
    warning_message = models.CharField(max_length = 300)

    class Meta:
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
        ("can_view", "Can view"),
        )

    def __unicode__(self):
        return self.row


class Supervisor(models.Model):

    language_english	= 'en'
    language_french		= 'fr'
    language_kinyarwanda	= 'rw'

    LANGUAGE_CHOICES = ( (language_english, "English"),
                (language_french, "French"),
                (language_kinyarwanda, "Kinyarwanda"))


    names = models.EmailField(max_length=150, null=True)
    dob = models.DateField(blank=True, null = True, help_text="Date Of Birth")
    area_level = models.CharField(max_length=13, null=True)
    village = models.ForeignKey(Village, null = True)
    cell = models.ForeignKey(Cell, null = True)
    sector = models.ForeignKey(Sector, null = True)
    health_centre = models.ForeignKey(HealthCentre, null = True)
    referral_hospital = models.ForeignKey(Hospital, null = True)
    district = models.ForeignKey(District, null = True)
    province = models.ForeignKey(Province, null = True)
    nation = models.ForeignKey(Nation, null = True)
    telephone_moh  = models.CharField(max_length=13, null=True, unique = True)
    email = models.EmailField(max_length=50, unique = True)
    national_id =  models.CharField(max_length=16, null=True, unique = True)
    language = models.CharField(max_length = 2, blank=True, null = True, choices= LANGUAGE_CHOICES, help_text="Select the preferred language to receive SMS")

    class Meta:
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
        ("can_view", "Can view"),
        )

    def __unicode__(self):
        return "Supervisor: %s" % (self.names)

    def get_connections(self):
        connections = None
        
        try:
            contact, created = Contact.objects.get_or_create(name = self.email)
            if self.language:    contact.language = self.language.lower()
            else:   contact.language = 'rw'

            backends = Backend.objects.all()
            for b in backends:
                try:
                    identity = self.telephone_moh if b.name != 'message_tester' else self.telephone_moh.replace('+','')
                    connection, created = Connection.objects.get_or_create(contact = contact, backend = b, identity = identity)
                    connection.save()
                except Exception,e:
                    continue
            
            contact.save()
            connections = Connection.objects.filter(contact = contact)
        except Exception, e:
            pass
            
        return connections

    def last_seen(self):
        """Returns the Python datetime that this Reporter was last seen,
            on any Connection. Before displaying in the WebUI, the output
           should be run through the XXX  filter, to make it prettier."""
        
        # comprehend a list of datetimes that this
        # reporter was last seen on each connection,
        # excluding those that have never seen them
        timedates = [
                        c.date
                        for c in Message.objects.filter( connection__in = Connection.objects.filter(contact__name = self.email))
                        if c.date is not None]
        
        # return the latest, or none, if they've
        # has never been seen on ANY connection
        return max(timedates) if timedates else None

    def connection(self):
        """Returns the connection object last used by this Reporter.
        The field is (probably) updated by app.py when receiving
        a message, so depends on _incoming_ messages only."""
        
        # TODO: add a "preferred" flag to connection, which then
        # overrides the last_seen connection as the default, here
        try:
            return Connection.objects.get(contact__name = self.email, contact = self.contact())#Connection.objects.get(contact__name = self.email, pk = Message.objects.filter( date = self.last_seen(), contact = self.contact())[0].connection.id)
        
        # if no connections exist for this reporter (how
        # did that happen?!), then just return None...
        except Connection.DoesNotExist:
            return None

    def contact(self):
        """Returns the connection object last used by this Reporter.
        The field is (probably) updated by app.py when receiving
        a message, so depends on _incoming_ messages only."""
        
        # TODO: add a "preferred" flag to connection, which then
        # overrides the last_seen connection as the default, here
        try:
            return Contact.objects.get(name = self.email)
        
        # if no connections exist for this reporter (how
        # did that happen?!), then just return None...
        except Contact.DoesNotExist:
            return None



##Signals

def ensure_connections_exists(sender, **kwargs):
    if kwargs.get('created', False):
        reporter = kwargs.get('instance')
        conns = reporter.get_connections()
        if conns:    return True
        else:   return False

post_save.connect(ensure_connections_exists, sender = Reporter)
post_save.connect(ensure_connections_exists, sender = Supervisor)

    
