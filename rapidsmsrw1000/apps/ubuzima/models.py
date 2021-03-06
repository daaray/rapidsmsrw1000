#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django.db import models
from django.contrib.auth.models import *
from rapidsmsrw1000.apps.ubuzima.mailer import Mailer
from rapidsmsrw1000.apps.chws.models import *
from django.utils.translation import ugettext as _
import datetime
from decimal import Decimal

def fosa_to_code(fosa_id):
    """Given a fosa id, returns a location code"""
    return "F" + fosa_id

def code_to_fosa(code):
    """Given a location code, returns the fosa id"""
    return code[1:]


class FieldCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name
    class Meta:
        
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
            ("can_view", "Can view"),
        )
    
 

class ReportType(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.name
    class Meta:
        
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
            ("can_view", "Can view"),
        ) 
    

class FieldType(models.Model):
    key = models.CharField(max_length=32, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(FieldCategory, related_name = "typecategory")
    has_value = models.BooleanField(default=False)
    kw = models.CharField(max_length=150)

    def __unicode__(self):
        return self.key
    class Meta:
        
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
            ("can_view", "Can view"),
        )
    
    
class Patient(models.Model):
    location = models.ForeignKey(HealthCentre, related_name = "patienthc")
    national_id = models.CharField(max_length = 20, unique = True)
    telephone = models.CharField(max_length = 13 , null = True)
    village    = models.ForeignKey(Village, related_name = "patvillage", null=True,  blank=True)
    cell = models.ForeignKey(Cell, related_name = 'patcell', null=True, blank=True)
    sector = models.ForeignKey(Sector, related_name = 'patsector', null=True, blank=True)
    district = models.ForeignKey(District, related_name = 'patdistrict', null=True, blank=True)
    province = models.ForeignKey(Province, related_name = 'patprovince', null=True, blank=True)
    nation = models.ForeignKey(Nation, related_name = 'patnation', null=True, blank=True)

    def __unicode__(self):
        return "%s" % self.national_id
    class Meta:
        
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
            ("can_view", "Can view"),
        )
        
    
    
class Report(models.Model):
    # Constants for our reminders.  Each reminder will be triggered this many days 
    # before the mother's EDD
    DAYS_ANC2 = 150
    DAYS_ANC3 = 60
    DAYS_ANC4 = 14
    DAYS_SUP_EDD = 30
    DAYS_EDD = 7
    DAYS_ON_THE_DOT = 0
    DAYS_WEEK_LATER = -7
    DAYS_PNC1 = 2
    DAYS_PNC2 = 6
    DAYS_PNC3 = 28
    DAYS_MONTH6 = 180
    DAYS_MONTH9 = 270
    DAYS_MONTH18 = 540
    DAYS_MONTH24 = 720

    reporter = models.ForeignKey(Reporter, related_name = "reportreporter")
    location = models.ForeignKey(HealthCentre, related_name = "reporthc")#location = models.ForeignKey(Location)
    village    = models.ForeignKey(Village, related_name = 'reportvillage', null=True, blank=True)#village = models.CharField(max_length=255, null=True)
    cell = models.ForeignKey(Cell, related_name = 'reportcell', null=True, blank=True)#cell = models.ForeignKey(Location, related_name = 'reportcell', null=True, blank=True)
    sector = models.ForeignKey(Sector, related_name = 'reportsector', null=True, blank=True)#sector = models.ForeignKey(Location, related_name = 'reportsector', null=True, blank=True)
    district = models.ForeignKey(District, related_name = 'reportdistrict', null=True, blank=True)#district = models.ForeignKey(Location, related_name = 'reportdistrict', null=True, blank=True)
    province = models.ForeignKey(Province, related_name = 'reportprovince', null=True, blank=True)#province = models.ForeignKey(Location, related_name = 'reportprovince', null=True, blank=True)
    nation = models.ForeignKey(Nation, related_name = 'reportnation', null=True, blank=True)#nation = models.ForeignKey(Location, related_name = 'reportnation', null=True, blank=True)
    #fields = models.ManyToManyField(Field)
    patient = models.ForeignKey(Patient , related_name = "reportpatient")
    type = models.ForeignKey(ReportType, related_name = "reporttype")

    # meaning of this depends on report type.. arr, should really do this as a field, perhaps as a munged int?
    date_string = models.CharField(max_length=10, null=True)

    # our real date if we have one complete with a date and time
    date = models.DateField(null=True)
    edd_date = models.DateField(null=True)
    bmi_anc1 = models.DecimalField(max_digits=10, decimal_places=5, null=True)
    edd_anc2_date = models.DateField(null=True)
    edd_anc3_date = models.DateField(null=True)
    edd_anc4_date = models.DateField(null=True)
    edd_pnc1_date = models.DateField(null=True)
    edd_pnc2_date = models.DateField(null=True)
    edd_pnc3_date = models.DateField(null=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
            ("can_view", "Can view"),
        )
    
    
    def __unicode__(self):
        return "Report id: %d type: %s patient: %s date: %s" % (self.pk, self.type.name, self.patient.national_id, self.date_string)

    def edd(self):
        try:	return Report.calculate_edd(self.date)
        except:	return None 
    
    def summary(self):
        summary = ""
        if self.date_string:
            summary += "Date=" + self.date_string

        if self.fields.all():
            if self.date_string: summary += ", "
            summary += ", ".join(map(lambda f: unicode(f), self.fields.all()))

        return summary
    def has_dups(self):
        if settings.TRAINING_ENV == False:
            return Report.objects.filter(type=self.type,patient=self.patient,date=self.date, reporter = self.reporter).exists()
        else:
            return False
    def rep_fields(self):
        flds = []
        rep_flds = self.fields.all()
        for fld in rep_flds:
            flds.append(fld)
        return flds

    def rep_fields_types(self):
        flds=self.rep_fields()
        types=[]
        for fld in flds:
            types.append(fld.type)
        return types
    		

    def rep_has_field_type(self, fldt):
        with_fldt=False
        if fldt in self.rep_fields_types():
            with_fldt=True
        return with_fldt

    def was_vaccinated(self):
        yes=False
        vacc=FieldCategory.objects.get(name='Vaccination')
        vacs=FieldType.objects.filter(category=vacc)
        for vac in vacs:
            if self.rep_has_field_type(vac):
                yes=True
                break
        return yes

    def get_vaccine(self):
        for x in self.fields.all():
            for vtp in FieldType.objects.filter(category=FieldCategory.objects.get(name='Vaccination')):
                if x.type==vtp:
                    return x.type 

    def was_vaccinated_with(self,vac):
        if self.get_vaccine() == vac:
            return True
        return False

    
    def is_home(self):
    	yes=False
    	ftp=FieldType.objects.get(key='ho')
    	if self.rep_has_field_type(ftp):
    		yes=True
    	return yes

    def is_hosp(self):
    	yes=False
    	ftp1=FieldType.objects.get(key='hp')
    	ftp2=FieldType.objects.get(key='cl')
    	if self.rep_has_field_type(ftp1) or self.rep_has_field_type(ftp2):
    		yes=True
    	return yes

    def is_route(self):
    	yes=False
    	ftp=FieldType.objects.get(key='or')
    	if self.rep_has_field_type(ftp):
    		yes=True
    	return yes

    def is_maternal_death(self):
    	if self.rep_has_field_type(FieldType.objects.get(key='md')):
    		return True
    	return False

    def is_child_death(self):
    	if self.rep_has_field_type(FieldType.objects.get(key='cd')):
    		return True
    	return False
    def is_newborn_death(self):
    	if self.rep_has_field_type(FieldType.objects.get(key='nd')):
    		return True
    	return False

    def has_no_toilet(self):
    	ftp=FieldType.objects.get(key='nt')
    	if self.rep_has_field_type(ftp):
    		return True
    	return False

    def has_no_hw(self):
    	ftp=FieldType.objects.get(key='nh')
    	if self.rep_has_field_type(ftp):
    		return True
    	return False

    def as_verbose_string(self):
        verbose = _("%s Report: ") % self.type.name
        verbose += _("Patient=%s, ") % self.patient
        verbose += _("Location=%s") % self.location
        if self.village:
            verbose += _(" (%s)") % self.village

        summary = self.summary()
        if summary:
            verbose += ", " + self.summary()
        return verbose

    def set_date_string(self, date_string):
        """
        Trap anybody setting the date_string and try to set the date from it.
        """
        self.date_string = date_string

        # try to parse the date.. dd/mm/yyyy
        try:
            self.date = datetime.datetime.strptime(date_string, "%d.%m.%Y").date()
    	    
        except ValueError,e:
            # no-op, just keep the date_string value
            pass


    @classmethod
    def get_reports_with_edd_in(cls, date, days, reminder_type):
        """
        Returns all the reports which have an EDD within ``days`` of ``date``.  The results
        will be filtered to not include items which have at least one reminder of the passed
        in type.
        """
        (start, end) = cls.calculate_reminder_range(date, days)

        # only check pregnancy reports
        # TODO: should we check others as well?  not sure what the date means in RISK reports
        # For now we assume everybody needs to register with a pregnancy report first
        preg_type = ReportType.objects.get(name = 'Pregnancy')

        # we only allow one report per patient
        reports = {}

        # filter our reports based on which have not received a reminder yet.
        # TODO: this is simple, but could get slow, at some point it may be worth
        # replacing it with some fancy SQL
        for report in Report.objects.filter(date__gte=start, date__lte=end, type=preg_type):
            if not report.reminders.filter(type=reminder_type) \
               and not Report.objects.filter( date__gte=start, date__lte=end, type__name = 'Birth', patient = report.patient)\
                 and not Field.objects.filter(report__patient = report.patient, type__key = 'mc'):
                reports[report.patient.national_id] = report

        return reports.values()
    
    @classmethod
    def calculate_edd(cls, last_menses):
        """
        Given the date of the last menses, figures out the expected delivery date
        """
            
        # first add seven days
        edd = last_menses + datetime.timedelta(7)

        # figure out if your year needs to be modified, anything later than march will
        # be the next year
        #	if edd.month > 3:
        #	    edd = edd.replace(year=edd.year+1, month=edd.month+9-12)
        #	else:
        #	    edd = edd.replace(month=edd.month+9)
        
        #	return edd

        neufmois = datetime.timedelta(days = 270)
        return edd + neufmois

    @classmethod
    def calculate_last_menses(cls, edd):
        """
        Given an EDD, figures out the last menses date.  This is basically the opposite
        function to calculate_edd
        """
        # figure out if your year needs to be modified, anything earlier than october
        # will be in the previous year
        #   if edd.month <= 9:
        #       last_menses = edd.replace(year=edd.year-1, month=edd.month-9+12)
        #   else:
        #       last_menses = edd.replace(month=edd.month-9)

        # now subtract 7 days
        #   last_menses = last_menses - datetime.timedelta(7)
        
        #   return last_menses
        return edd - datetime.timedelta(days = 277)

    @classmethod
    def calculate_reminder_range(cls, date, days):
        """
        Passed in a day (of today), figures out the range for the menses dates for
        our reminder.  The ``days`` variable is the number of days before delivery
        we want to figure out the date for.  (bracketed by 2 days each way)
        
        """
        # figure out the expected delivery date
        edd = date + datetime.timedelta(days)

        # calculate the last menses
        last_menses = cls.calculate_last_menses(edd)

        # bracket in either direction
        start = last_menses - datetime.timedelta(2)
        end = last_menses + datetime.timedelta(2)
    
        return (start, end)

    def is_risky(self):
        risk = self.fields.filter(type__category__name = 'Risk Codes').exclude(type__key = 'np')
        return risk.exists()

    def is_red(self):
        if self.type == ReportType.objects.get(name = 'Red Alert'):  return True
        return False

    def is_death(self):
        risk = self.fields.filter(type__key__in = ['md','nd','cd'])
        return risk.exists()

    def is_high_risky_preg(self):
    	risk = Report.objects.filter( patient = self.patient, fields__in = Field.objects.filter( type__in = FieldType.objects.filter(key__in =['ps','ds','sl','ja','fp','un','sa','co','he','pa','ma','sc','la'])))
    	return risk.exists()

    def show_edd(self):
        preg = Report.objects.filter(type__name = 'Pregnancy', patient = self.patient).order_by('-date')
    	if preg.exists():   return self.calculate_edd(self.date)
        else :  return None

    def get_child_id(self):
    	try:	return { 'chino': int(self.fields.get(type__key = "child_number").value), 'dob': self.date, 'mother': self.patient }
    	except:	return None
    def get_field(self,key):
    	try:	return self.fields.get(type__key = key)
    	except:	return None
    def get_sex(self):
    	try:	return self.fields.filter(type__key__in = ['bo','gi'])[0]
    	except:	return None	

    def get_child(self):
    	try:
            
    		chino, dob, mother = self.get_child_id()['chino'], self.get_child_id()['dob'], self.get_child_id()['mother']
    		chihe = Report.objects.filter( type__name = "Child Health", date = dob , patient = mother , fields__in = Field.objects.filter(type__key = 'child_number',   value = Decimal(chino))).order_by('created')

    		ans, track = {},[]
    		for r in chihe:
    			track.append( {'date': r.created, 'risk': r.fields.filter(type__category__name = 'Risk'), 'weight': r.get_field('child_weight'), 'muac': r.get_field('muac') })

    		ans['id'] = self.get_child_id()
    		ans['birth'] = {'date': self.date, 'risk': self.fields.filter(type__category__name = 'Risk'), 'weight': self.get_field('child_weight'), 'muac': self.get_field('muac'), 'sex': self.get_sex() }
    		ans['track'] = track
		ans['log'] = chihe
   		return ans
    	except:	None

    def set_preg_edd_dates(self, given_date):
    	try:
    	    	self.edd_date =  self.calculate_edd(given_date)
    	    	self.edd_anc2_date =  self.edd_date - datetime.timedelta(self.DAYS_ANC2)
    	    	self.edd_anc3_date =  self.edd_date - datetime.timedelta(self.DAYS_ANC3)
    	    	self.edd_anc4_date =  self.edd_date - datetime.timedelta(self.DAYS_ANC4)
    	    	
    	except:	return None
    def set_pnc_edd_dates(self, given_date):
    	try:
    	    	self.edd_pnc1_date =  given_date + datetime.timedelta(self.DAYS_PNC1)
    	    	self.edd_pnc2_date =  given_date + datetime.timedelta(self.DAYS_PNC2)
    	    	self.edd_pnc3_date =  given_date + datetime.timedelta(self.DAYS_PNC3)
    	except:	return None
    
    	
    	    
class TriggeredText(models.Model):
    """ Represents an automated text response that is returned to the CHW, SUP or district SUP based 
        on a set of matching action codes. """

    DESTINATION_CHW = 'CHW'
    DESTINATION_SUP = 'SUP'
    DESTINATION_DIS = 'DIS'
    DESTINATION_AMB = 'AMB'

    DESTINATION_CHOICES = ( (DESTINATION_CHW, "Community Health Worker"),
                            (DESTINATION_SUP, "Clinic Supervisor"),
                            (DESTINATION_DIS, "District Supervisor"),
                            (DESTINATION_AMB, "Ambulance"))
    
    name = models.CharField(max_length=128)
    destination = models.CharField(max_length=3, choices=DESTINATION_CHOICES,
                                   help_text="Where this text will be sent to when reports match all triggers.")

    description = models.TextField()
    
    message_kw = models.CharField(max_length=160)
    message_fr = models.CharField(max_length=160)
    message_en = models.CharField(max_length=160)

    triggers = models.ManyToManyField(FieldType, related_name = "triggercode",
                                      help_text="This trigger will take effect when ALL triggers match the report.")

    active = models.BooleanField(default=True)
    
    class Meta:
        
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
            ("can_view", "Can view"),
        )

    def trigger_summary(self):
        return ", ".join(map(lambda t: t.description, self.triggers.all()))
    
    
    def __unicode__(self):
        return self.name

    @classmethod
    def get_triggers_for_report(cls, report):
        """
        Returns which trigger texts match this report.
        It is up to the caller to actually send the messages based on the triggers returned.
        """
        types = []
        for field in report.fields.all():
            types.append(field.type.pk)
               
        # these are the texts which may get activated
        texts = TriggeredText.objects.filter(triggers__in=types).distinct().order_by('id')

        # triggers that should be sent back, one per destination
        matching_texts = []
            
        # for each trigger text, see whether we should be triggered by it
        for text in texts:
            matching = True
            
            for trigger in text.triggers.all():
                found = False

                for field in report.fields.all():
                    if trigger.pk == field.type.pk:
                        found = True
                        break
                    
                # not found?  this won't trigger
                if not found:
                    matching = False
            
            if matching:
                matching_texts.append(text)

        # sort the texts, first by number of triggers (more specific texts should be triggered
        # before vague ones) then by id (earliest triggers should take precedence)
        matching_texts.sort(key=lambda tt: "%04d_%06d" % (len(tt.triggers.all()), 100000 - tt.pk))
        matching_texts.reverse()

        # now build a map containing only one trigger per destination
        per_destination = {}
        for tt in matching_texts:
            if not tt.destination in per_destination:
                per_destination[tt.destination] = tt
                
        # return our trigger texts
        matching_list = per_destination.values()
        matching_list.sort(key=lambda tt: tt.pk)
        return matching_list

class ReminderType(models.Model):
    """
    Simple models to keep track of the differen kinds of reminders.
    """

    name = models.CharField(max_length=255)

    message_kw = models.CharField(max_length=160)
    message_fr = models.CharField(max_length=160)
    message_en = models.CharField(max_length=160)

    class Meta:
        
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
            ("can_view", "Can view"),
        )

    def __unicode__(self):
        return self.name
    

class Field(models.Model):
    location = models.ForeignKey(HealthCentre, related_name = "fieldhc", null =True)
    type = models.ForeignKey(FieldType, related_name = "fieldtype")
    report = models.ForeignKey(Report, related_name = "fields")
    village = models.ForeignKey(Village, related_name = 'fieldvillage', null=True)#village = models.CharField(max_length=255, null=True)
    cell = models.ForeignKey(Cell, related_name = 'fieldcell', null=True)#cell = models.ForeignKey(Location, related_name = 'fieldcell', null=True)
    sector = models.ForeignKey(Sector, related_name = 'fieldsector', null=True)#sector = models.ForeignKey(Location, related_name = 'fieldsector', null=True)
    district = models.ForeignKey(District, related_name = 'fielddistrict', null=True)#district = models.ForeignKey(Location, related_name = 'fielddistrict', null=True)
    province = models.ForeignKey(Province, related_name = 'fieldprovince', null=True)#province = models.ForeignKey(Location, related_name = 'fieldprovince', null=True)
    nation = models.ForeignKey(Nation, related_name = 'fieldnation', null=True)#nation = models.ForeignKey(Location, related_name = 'fieldnation', null=True)
    value = models.DecimalField(max_digits=10, decimal_places=5, null=True)
    creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
            ("can_view", "Can view"),
        )
    
    def __unicode__(self):
        if self.value:
            return "%s=%.2f" % (_(self.type.description), self.value)
        else:
            return "%s" % _(self.type.description)
    class Meta:
        unique_together = ('type', 'report')

    @classmethod
    def get_risk_fieldtypes(cls):
    	codes = FieldType.objects.filter(key__in = ['af', 'ch', 'ci', 'cm', 'co', 'di', 'ds', 'fe', 'fp', 'he', 'hy', 'ja', 'ma', 'mc',\
						 'ns', 'oe', 'pa', 'pc', 'ps', 'rb', 'sa', 'sc', 'sl', 'un', 'vo', 'la'])
    	return codes

    def get_report(self):
   	try:
   		return self.report_set.all()[0]
    	except: return None

class Reminder(models.Model):
    """
    Logs reminders that have been sent.  We use this both for tracking and so that we do
    not send more than one reminder at a time.
    """
    location = models.ForeignKey(HealthCentre, related_name = "reminderhc")
    reporter = models.ForeignKey(Reporter, related_name = "reminderreporter")
    report = models.ForeignKey(Report, related_name="reminders", null=True)
    type = models.ForeignKey(ReminderType, related_name = "remindertype")
    village = models.ForeignKey(Village, related_name = 'remindervillage', null=True)#village = models.CharField(max_length=255, null=True)
    cell = models.ForeignKey(Cell, related_name = 'remindercell', null=True)#cell = models.ForeignKey(Location, related_name = 'remindercell', null=True)
    sector = models.ForeignKey(Sector, related_name = 'remindersector', null=True)#sector = models.ForeignKey(Location, related_name = 'remindersector', null=True)
    district = models.ForeignKey(District, related_name = 'reminderdistrict', null=True)#district = models.ForeignKey(Location, related_name = 'reminderdistrict', null=True)
    province = models.ForeignKey(Province, related_name = 'reminderprovince', null=True)#province = models.ForeignKey(Location, related_name = 'reminderprovince', null=True)
    nation = models.ForeignKey(Nation, related_name = 'remindernation', null=True)#nation = models.ForeignKey(Location, related_name = 'remindernation', null=True)
    date = models.DateTimeField()

    class Meta:
        
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
            ("can_view", "Can view"),
        )
    
    def __unicode__(self):
			return "Reminder Type:%s   Sent:(%s)   Patient:%s   Location:%s   Reporter:%s" % (self.type, self.date,self.report.patient if self.report else None,self.reporter.health_centre, self.reporter.connection().identity)

    @classmethod
    def get_expired_reporters(cls, today):
        # we'll check anybody who hasn't been seen in between 15 and 45 days
        expired_start = today - datetime.timedelta(45)
        expired_end = today - datetime.timedelta(15)

        # reporter reminder type
        expired_type = ReminderType.objects.get(name = "Inactive Reporter")
        inactive = [ r for r in Reporter.objects.all() if r.is_expired() ]

        reporters = set()

        for reporter in inactive:
            # get our most recent reminder
            reminders = Reminder.objects.filter(reporter=reporter, type=expired_type).order_by('-date')

            # we've had a previous reminder
            if reminders:
                last_reminder = reminders[0]
                # if we were last seen before the reminder, we've already been reminded, skip over
                try:
                    if reporter.last_seen() < last_reminder.date:   continue
                except: pass

            # otherwise, pop this reporter on
            reporters.add(reporter)

        return reporters





class Refusal(models.Model):
    'This represents refusals to give a health agent information. We keep instead a reference to the reporter, in order to follow up, if necessary.'

    location = models.ForeignKey(HealthCentre, related_name = "refusalhc")
    reporter = models.ForeignKey(Reporter, related_name = 'refusalreporter')
    refid    = models.TextField()
    village = models.ForeignKey(Village, related_name = 'refusalvillage', null=True)#village = models.CharField(max_length=255, null=True)
    cell = models.ForeignKey(Cell, related_name = 'refusalcell', null=True)#cell = models.ForeignKey(Location, related_name = 'refusalcell', null=True)
    sector = models.ForeignKey(Sector, related_name = 'refusalsector', null=True)#sector = models.ForeignKey(Location, related_name = 'refusalsector', null=True)
    district = models.ForeignKey(District, related_name = 'refusaldistrict', null=True)#district = models.ForeignKey(Location, related_name = 'refusaldistrict', null=True)
    province = models.ForeignKey(Province, related_name = 'refusalprovince', null=True)#province = models.ForeignKey(Location, related_name = 'refusalprovince', null=True)
    nation = models.ForeignKey(Nation, related_name = 'refusalnation', null=True)#nation = models.ForeignKey(Location, related_name = 'refusalnation', null=True)
    created = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.reporter.telephone_moh

    class Meta:
        
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
            ("can_view", "Can view"),
        )   

class Departure(models.Model):
    'This represents departure to give a health agent information. We keep instead a reference to the reporter, in order to follow up, if necessary.'

    location = models.ForeignKey(HealthCentre, related_name = "departurehc")
    reporter = models.ForeignKey(Reporter, related_name = 'depmother')
    depid    = models.TextField()
    dob = models.DateField(null=True)
    child_number = models.IntegerField(null = True)
    village = models.ForeignKey(Village, related_name = 'depvillage', null=True)#village = models.CharField(max_length=255, null=True)
    cell = models.ForeignKey(Cell, related_name = 'depcell', null=True)#cell = models.ForeignKey(Location, related_name = 'depcell', null=True)
    sector = models.ForeignKey(Sector, related_name = 'depsector', null=True)#sector = models.ForeignKey(Location, related_name = 'depsector', null=True)
    district = models.ForeignKey(District, related_name = 'depdistrict', null=True)#district = models.ForeignKey(Location, related_name = 'depdistrict', null=True)
    province = models.ForeignKey(Province, related_name = 'depprovince', null=True)#province = models.ForeignKey(Location, related_name = 'depprovince', null=True)
    nation = models.ForeignKey(Nation, related_name = 'depnation', null=True)#nation = models.ForeignKey(Location, related_name = 'depnation', null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.reporter.telephone_moh

    class Meta:
        
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
            ("can_view", "Can view"),
        )

    

class ErrorType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    def __unicode__(self):
        return self.description
    
    class Meta:
        
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
            ("can_view", "Can view"),
        )
    

class ErrorNote(models.Model):
    '''This model is used to record errors made by people sending messages into the system, to facilitate things like studying which format structures are error-prone, and which reporters make the most errors, and other things like that.'''

    errmsg  = models.TextField()
    type = models.ForeignKey(ErrorType, related_name='errorcategory')
    location = models.ForeignKey(HealthCentre, related_name = "errorhc")
    village = models.ForeignKey(Village, related_name = 'errorvillage', null=True)#village = models.CharField(max_length=255, null=True)
    cell = models.ForeignKey(Cell, related_name = 'errorcell', null=True)#cell = models.ForeignKey(Location, related_name = 'errorcell', null=True)
    sector = models.ForeignKey(Sector, related_name = 'errorsector', null=True)#sector = models.ForeignKey(Location, related_name = 'errorsector', null=True)
    district = models.ForeignKey(District, related_name = 'errordistrict', null=True)#district = models.ForeignKey(Location, related_name = 'errordistrict', null=True)
    province = models.ForeignKey(Province, related_name = 'errorprovince', null=True)#province = models.ForeignKey(Location, related_name = 'errorprovince', null=True)
    nation = models.ForeignKey(Nation, related_name = 'errornation', null=True)#nation = models.ForeignKey(Location, related_name = 'errornation', null=True)
    errby   = models.ForeignKey(Reporter, null =True , related_name = 'erringreporter')
    identity = models.CharField(max_length=13, null=True)
    created = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return '%s (%s): "%s"' % (str(self.errby.connection().identity), str(self.created), str(self.errmsg))

    def __int__(self):
        return self.id

    class Meta:
        
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
            ("can_view", "Can view"),
        )
    

class UserLocation(models.Model):
    """This model is used to help the system to know where the user who is trying to access this information is from"""
    user=models.ForeignKey(User, related_name = "hcuser")
    health_centre = models.ForeignKey(HealthCentre, related_name = "userhc", null=True, blank = True)
    referral_hospital = models.ForeignKey(Hospital, related_name = "userhospital", null=True, blank = True)
    village = models.ForeignKey(Village, related_name = 'uservillage', null=True, blank = True)
    cell = models.ForeignKey(Cell, related_name = 'usercell', null=True, blank = True)
    sector = models.ForeignKey(Sector, related_name = 'usersector', null=True, blank = True)
    district = models.ForeignKey(District, related_name = 'userdistrict', null=True, blank = True)
    province = models.ForeignKey(Province, related_name = 'userprovince', null=True, blank = True)
    nation = models.ForeignKey(Nation, related_name = 'usernation', null=True, blank = True)

    class Meta:
        
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
            ("can_view", "Can view"),
        )

    def __unicode__(self):
        return '%s' % (str(self.user))

    def __int__(self):
        return self.id
	

class TriggeredAlert(models.Model):
    """
                        Logs alerts that have been sent. """

    RESPONSE_YES = 'YES'
    RESPONSE_NO = 'NO'
    RESPONSE_PO = 'PO'
    RESPONSE_NR = 'NR'
    RESPONSE_CHOICES = ( (RESPONSE_YES, "Responded"),
                            (RESPONSE_NO, "Not Responded"),
			    (RESPONSE_PO, "Positive Outcome"),
                            (RESPONSE_NR, "Not Required or No Returns"))
    location = models.ForeignKey(HealthCentre, related_name = "alerthc")
    reporter = models.ForeignKey(Reporter, related_name = "alertreporter")
    report = models.ForeignKey(Report, related_name="alerts", null=True)
    trigger=models.ForeignKey(TriggeredText, related_name = "alerttext")
    village = models.ForeignKey(Village, related_name = 'triggervillage', null=True)
    cell = models.ForeignKey(Cell, related_name = 'triggeralertcell', null=True)
    sector = models.ForeignKey(Sector, related_name = 'triggeralertsector', null=True)
    district = models.ForeignKey(District, related_name = 'triggeralertdistrict', null=True)
    province = models.ForeignKey(Province, related_name = 'triggeralertprovince', null=True)
    nation = models.ForeignKey(Nation, related_name = 'triggeralertnation', null=True)
    date = models.DateTimeField(auto_now_add=True)
    response = models.CharField(max_length=3, choices=RESPONSE_CHOICES, default = "NR",
                                   help_text="These choices will be used only where applicable, otherwise choice is initialized to Not Required.")

    class Meta:
        
        # define a permission for this app to use the @permission_required
        # in the admin's auth section, we have a group called 'manager' whose
        # users have this permission -- and are able to see this section
        permissions = (
            ("can_view", "Can view"),
        )

    def __unicode__(self):
		return '%s : "%s"' % (str(self.id), str(self.trigger))

    def __int__(self):
    	return self.id
    


def ensure_report_correct(sender, **kwargs):
    if kwargs.get('created', False):
        report = kwargs.get('instance')
        ##Patient details correct
        patient = report.patient
        patient.location = report.location
        patient.village = report.reporter.village
        patient.cell = report.reporter.cell
        patient.sector = report.reporter.sector
        patient.district = report.reporter.district
        patient.province = report.reporter.province
        patient.nation = report.reporter.nation
        patient.save()

        ##Report details correct
        report.village = report.reporter.village
        report.cell = report.reporter.cell
        report.sector = report.reporter.sector
        report.district = report.reporter.district
        report.province = report.reporter.province
        report.nation = report.reporter.nation
        report.save()

        
        if report:    return True
        else:   return False

def ensure_field_correct(sender, **kwargs):
    if kwargs.get('created', False):
        field = kwargs.get('instance')
        ##Field details correct
        reporter = field.report.reporter
        field.location = field.report.location
        field.village = reporter.village
        field.cell = reporter.cell
        field.sector = reporter.sector
        field.district = reporter.district
        field.province = reporter.province
        field.nation = reporter.nation
        field.save()

def ensure_refusal_correct(sender, **kwargs):
    if kwargs.get('created', False):
        refusal = kwargs.get('instance')
        ##Field details correct
        reporter = refusal.reporter
        
        refusal.village = reporter.village
        refusal.cell = reporter.cell
        refusal.sector = reporter.sector
        refusal.district = reporter.district
        refusal.province = reporter.province
        refusal.nation = reporter.nation
        refusal.save()

def ensure_departure_correct(sender, **kwargs):
    if kwargs.get('created', False):
        dep = kwargs.get('instance')
        ##Field details correct
        reporter = dep.reporter
        
        dep.village = reporter.village
        dep.cell = reporter.cell
        dep.sector = reporter.sector
        dep.district = reporter.district
        dep.province = reporter.province
        dep.nation = reporter.nation
        dep.save()


def send_alert_mails(sender, **kwargs):
    # the object which is saved can be accessed via kwargs 'instance' key.
    obj = kwargs['instance']
    Mailer().user_reg_notify(obj.user) #send email after a user created#print 'the object is now saved.',obj,obj.user
    # ...do something else...

post_save.connect(ensure_report_correct, sender = Report)
post_save.connect(ensure_field_correct, sender = Field)
post_save.connect(ensure_refusal_correct, sender = Refusal)
post_save.connect(ensure_departure_correct, sender = Departure)
post_save.connect(send_alert_mails,sender=UserLocation)


