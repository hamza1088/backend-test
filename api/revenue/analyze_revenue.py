from fastapi import APIRouter, Query
from sqlalchemy import func
from models import Sale
from datetime import date
from database import SessionLocal


router = APIRouter()


@router.get("/revenue/daily")
async def daily_revenue(
    date: date = Query(..., description="Date for revenue analysis")
):
    db = SessionLocal()
    try:
        daily_revenue = db.query(func.date(Sale.sale_date).label("date"), func.sum(Sale.revenue).label("total_revenue")). \
            filter(func.date(Sale.sale_date) == date).group_by(func.date(Sale.sale_date)).all()

        formatted_daily_revenue = [{"date": str(row.date), "total_revenue": row.total_revenue} for row in daily_revenue]

        return formatted_daily_revenue
    finally:
        db.close()


@router.get("/revenue/weekly")
async def weekly_revenue(
    start_date: date = Query(..., description="Start date of the week"),
    end_date: date = Query(..., description="End date of the week")
):
    db = SessionLocal()
    try:
        weekly_revenue = db.query(func.week(Sale.sale_date).label("week"), func.sum(Sale.revenue).label("total_revenue")). \
            filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date).group_by(func.week(Sale.sale_date)).all()

        formatted_weekly_revenue = [{"week": int(row.week), "total_revenue": float(row.total_revenue)} for row in weekly_revenue]

        return formatted_weekly_revenue
    finally:
        db.close()


@router.get("/revenue/monyhly")
async def monthly_revenue(
    start_date: date = Query(..., description="Start date of the month"),
    end_date: date = Query(..., description="End date of the month"),
):
    db = SessionLocal()
    try:
        monthly_revenue = db.query(func.year(Sale.sale_date).label("year"), func.month(Sale.sale_date).label("month"), func.sum(Sale.revenue).label("total_revenue")). \
            filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date).group_by(func.year(Sale.sale_date), func.month(Sale.sale_date)).all()

        formatted_monthly_revenue = [{"year": int(row.year), "month": int(row.month), "total_revenue": float(row.total_revenue)} for row in monthly_revenue]

        return formatted_monthly_revenue
    finally:
        db.close()



@router.get("/revenue/anually")
async def annual_revenue(
    start_date: date = Query(..., description="Start date of the year"),
    end_date: date = Query(..., description="End date of the year"),
):
    db = SessionLocal()
    try:
        annual_revenue = db.query(func.year(Sale.sale_date).label("year"), func.sum(Sale.revenue).label("total_revenue")). \
            filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date).group_by(func.year(Sale.sale_date)).all()

        formatted_annual_revenue = [{"year": int(row.year), "total_revenue": float(row.total_revenue)} for row in annual_revenue]

        return formatted_annual_revenue
    finally:
        db.close()
















