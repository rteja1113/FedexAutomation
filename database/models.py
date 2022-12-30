import django.db.utils
import xlrd
from collections import Counter
import logging
import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from database.constants import DB_COL_OFFESET_ROUTE_SPLIT
# Create your models here.

logging.basicConfig(level=logging.DEBUG)


class DailyService(models.Model):
    date = models.DateField()
    # SERVICE AREA DETAILS
    service_area_id = models.PositiveIntegerField(null=True)
    wa_name = models.CharField(null=True, max_length=20)
    vehicle_id = models.PositiveIntegerField(null=True)
    driver_name = models.CharField(null=True, max_length=40)
    wa_id = models.PositiveIntegerField(null=True)
    scanned_pkgs = models.PositiveIntegerField(null=True)

    # PRELOAD DATA
    delivery_stops = models.PositiveIntegerField(null=True)
    pickup_stops = models.PositiveIntegerField(null=True)
    diff = models.BigIntegerField(null=True)
    actual_delivered_stops = models.PositiveIntegerField(null=True)

    # P&D RESULTS
    actual_delivered_pkgs = models.PositiveIntegerField(null=True)
    actual_pickup_stops = models.PositiveIntegerField(null=True)
    actual_pickup_packages = models.PositiveIntegerField(null=True)
    ils_percentage = models.FloatField(null=True)
    ils_impact_pkgs = models.PositiveIntegerField(null=True)
    non_delivered_stops = models.PositiveIntegerField(null=True)
    code_85 = models.PositiveIntegerField(null=True)
    all_status_code_pkgs = models.PositiveIntegerField(null=True)

    # STATUS CODE PACKAGES
    pl_ml = models.PositiveIntegerField(null=True)
    dna = models.PositiveIntegerField(null=True)
    snd_agn = models.PositiveIntegerField(null=True)
    excs = models.PositiveIntegerField(null=True)
    vsa_vs_start_diff = models.PositiveIntegerField(null=True)
    return_scans_percentage = models.FloatField(null=True)
    miles = models.PositiveIntegerField(null=True)

    # DOT HOURS AND MILES
    on_road_hours = models.CharField(null=True, max_length=10)
    on_duty_hours = models.CharField(null=True, max_length=10)
    pot_dot_hrs_viols = models.CharField(null=True, max_length=10)
    next_avail_on_duty = models.CharField(null=True, max_length=10)
    pot_miss_pus = models.CharField(null=True, max_length=10)

    # PU PERF
    e_and_l_pus = models.CharField(null=True, max_length=10)
    req_sign = models.PositiveIntegerField(null=True)

    # PREMIUM SERVICES
    date_certain = models.CharField(null=True, max_length=10)
    evening = models.CharField(null=True, max_length=10)
    appt = models.CharField(null=True, max_length=10)

    # route
    is_route_split = models.BooleanField(null=False, default=False)
    parent_route_id = models.PositiveIntegerField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["date", "vehicle_id", "driver_name", "actual_delivered_stops", "parent_route_id"], name="unique_date_vehicle_id"
            )
        ]
        ordering = ['date', 'vehicle_id']


    def print_on_road_hours(self):
        hours, minutes = self.on_road_hours.split(":")
        print(f"{hours} hours and {minutes} minutes")

    @staticmethod
    def is_end_of_data(xl_sheet, row_counter):
        if "Contract" in xl_sheet.cell_value(row_counter, 0):
            print("contract found")
            return True
        else:
            return False

    @staticmethod
    def parse_date(raw_text):
        raw_date = raw_text.split("-")[-1].strip()
        return datetime.datetime.strptime(raw_date, "%m/%d/%Y").date()

    @classmethod
    def _find_parent_rows(cls, xls_file, row_counter):
        wa_ids = [None]*row_counter

        while not cls.is_end_of_data(xls_file, row_counter):
            wa_id = int(xls_file.cell_value(row_counter, 4).strip())
            wa_ids.append(wa_id)
            row_counter += 1

        wa_id_counter = Counter(wa_ids)
        parent_row_ids = [wa_ids.index(k) for k,v in wa_id_counter.items() if v > 1]
        print("parent rows : ", parent_row_ids)
        return parent_row_ids

    @classmethod
    def from_xls_file(cls, xls_file):
        book = xlrd.open_workbook(xls_file)
        sh = book.sheet_by_index(0)
        date = cls.parse_date(sh.cell_value(0, 0))
        prev_wa_id = None
        row_counter = 4
        parent_rows = cls._find_parent_rows(sh, row_counter)

        while not cls.is_end_of_data(sh, row_counter):
            print(row_counter)
            # print('-'+sh.cell_value(row_counter, 2) + '-')
            if sh.cell_value(row_counter, 2).strip() == "":
                logging.info("skipping this row as it does not have any data")
                row_counter += 1
                continue



            wa_id = int(sh.cell_value(row_counter, 4).strip())
            if prev_wa_id == wa_id:
                col_offset = DB_COL_OFFESET_ROUTE_SPLIT
                parent_id = ds.parent_route_id if ds.parent_route_id is not None else ds.id
            else:
                col_offset = 0
                parent_id = None

            is_route_split = True if row_counter in parent_rows else False

            # SERVICE AREA DETAILS
            svc_area = int(sh.cell_value(row_counter, 0))
            wa_name = sh.cell_value(row_counter, 1)
            if len(sh.cell_value(row_counter, 2).strip().split()) == 2:
                vehicle_id = int(sh.cell_value(row_counter, 2).strip().split()[1])
            else:
                vehicle_id = int(sh.cell_value(row_counter, 2).strip())

            driver_name = sh.cell_value(row_counter, 3)
            wa_id = int(sh.cell_value(row_counter, 4).strip())

            prev_wa_id = wa_id

            if sh.cell_value(row_counter, 5).strip() == "":
                vscan_pkgs = None
            else:
                vscan_pkgs = int(sh.cell_value(row_counter, 5).strip())

            # PRELOAD DATA
            if sh.cell_value(row_counter, 6).strip() == "":
                del_stps = None
            else:
                del_stps = int(sh.cell_value(row_counter, 6).strip())

            if sh.cell_value(row_counter, 7).strip() == "":
                pu_stps = None
            else:
                pu_stps = int(sh.cell_value(row_counter, 7).strip())

            if sh.cell_value(row_counter, 8).strip() == "":
                diff = 0
            else:
                diff = int(sh.cell_value(row_counter, 8).strip())

            if sh.cell_value(row_counter, 9 + col_offset).strip() == "":
                act_del_stops = 0
            else:
                act_del_stops = int(sh.cell_value(row_counter, 9 + col_offset).strip())

            # T&D RESULTS
            if sh.cell_value(row_counter, 10 + col_offset).strip() == "":
                act_del_pkgs = 0
            else:
                act_del_pkgs = int(sh.cell_value(row_counter, 10 + col_offset).strip())

            if sh.cell_value(row_counter, 11 + col_offset).strip() == "":
                act_pu_stops = 0
            else:
                act_pu_stops = int(sh.cell_value(row_counter, 11+col_offset))

            if sh.cell_value(row_counter, 12+col_offset).strip() == "":
                act_pu_pkgs = 0
            else:
                act_pu_pkgs = int(sh.cell_value(row_counter, 12+col_offset))

            if "%" in sh.cell_value(row_counter, 13+col_offset):
                ils_perc = sh.cell_value(row_counter, 13+col_offset)[:-1]
            else:
                if sh.cell_value(row_counter, 13+col_offset) == "":
                    ils_perc = None
                else:
                    ils_perc = sh.cell_value(row_counter, 13+col_offset)

            if sh.cell_value(row_counter, 14+col_offset).strip() == "":
                ils_impact_pkgs = None
            else:
                ils_impact_pkgs = int(sh.cell_value(row_counter, 14+col_offset).strip())

            if sh.cell_value(row_counter, 15+col_offset).strip() == "":
                non_dlvd_stops = None
            else:
                non_dlvd_stops = int(sh.cell_value(row_counter, 15+col_offset).strip())

            if sh.cell_value(row_counter, 16+col_offset).strip() == "":
                code_85 = None
            else:
                code_85 = int(sh.cell_value(row_counter, 16+col_offset).strip())

            if sh.cell_value(row_counter, 17+col_offset).strip() == "":
                all_status_code_pkgs = 0
            else:
                all_status_code_pkgs = int(sh.cell_value(row_counter, 17+col_offset).strip())

            # STATUS CODE PACKAGES
            if sh.cell_value(row_counter, 18+col_offset).strip() == "":
                pl_ml = 0
            else:
                pl_ml = int(sh.cell_value(row_counter, 18+col_offset).strip())

            if sh.cell_value(row_counter, 19+col_offset).strip() == "":
                dna = None
            else:
                dna = int(sh.cell_value(row_counter, 19+col_offset).strip())

            if sh.cell_value(row_counter, 20+col_offset).strip() == "":
                snd_agn = None
            else:
                snd_agn = int(sh.cell_value(row_counter, 20+col_offset).strip())

            if sh.cell_value(row_counter, 21+col_offset).strip() == "":
                excs = None
            else:
                excs = int(sh.cell_value(row_counter, 21+col_offset).strip())

            if sh.cell_value(row_counter, 22+col_offset).strip() == "":
                vsa_vs_start_diff = 0
            else:
                vsa_vs_start_diff = int(sh.cell_value(row_counter, 22+col_offset).strip())

            if "%" in sh.cell_value(row_counter, 23+col_offset):
                return_scans_perc = float(sh.cell_value(row_counter, 23+col_offset)[:-1].replace(",", ""))
            else:
                return_scans_perc = 0.0

            if sh.cell_value(row_counter, 24+col_offset).strip() == "":
                miles = None
            else:
                miles = int(sh.cell_value(row_counter, 24+col_offset).strip())

            on_road_hours = sh.cell_value(row_counter, 25+col_offset)
            on_duty_hours = sh.cell_value(row_counter, 26+col_offset)

            pot_dot_hrs_viols = sh.cell_value(row_counter, 27+col_offset)
            next_avail_on_duty = sh.cell_value(row_counter, 28+col_offset)
            pot_miss_pus = sh.cell_value(row_counter, 29+col_offset)

            el_pus = sh.cell(row_counter, 30+col_offset)
            if sh.cell_value(row_counter, 31+col_offset).strip() == "":
                req_sign = None
            else:
                req_sign = int(sh.cell_value(row_counter, 31+col_offset))



            ds = cls(
            date=date,
            service_area_id=svc_area,
            wa_name=wa_name,
            vehicle_id=vehicle_id,
            driver_name=driver_name,
            wa_id=wa_id,
            scanned_pkgs=vscan_pkgs,
            delivery_stops=del_stps,
            pickup_stops=pu_stps,
            diff=diff,
            actual_delivered_pkgs=act_del_pkgs,
            actual_delivered_stops =act_del_stops,
            actual_pickup_stops=act_pu_stops,
            actual_pickup_packages=act_pu_pkgs,
            ils_percentage=ils_perc,
            ils_impact_pkgs=ils_impact_pkgs,
            non_delivered_stops=non_dlvd_stops,
            code_85=code_85,
            all_status_code_pkgs=all_status_code_pkgs,
            pl_ml =pl_ml,
            dna =dna,
            snd_agn =snd_agn,
            excs =excs,
            vsa_vs_start_diff =vsa_vs_start_diff,
            return_scans_percentage=return_scans_perc,
            miles=miles,
            on_road_hours=on_road_hours,
            on_duty_hours=on_duty_hours,
            pot_dot_hrs_viols=pot_dot_hrs_viols,
            next_avail_on_duty=next_avail_on_duty,
            pot_miss_pus=pot_miss_pus,
            e_and_l_pus=el_pus,
            req_sign=req_sign,
            date_certain=None,
            evening=None,
            appt=None,
            parent_route_id=parent_id,
            is_route_split=is_route_split
            )
            try:
                ds.save()
            except django.db.utils.IntegrityError:
                logging.info(f"Encountered a duplicate row at {row_counter}, skipping this one")

            row_counter += 1