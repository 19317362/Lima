//###########################################################################
// This file is part of LImA, a Library for Image Acquisition
//
// Copyright (C) : 2009-2011
// European Synchrotron Radiation Facility
// BP 220, Grenoble 38043
// FRANCE
//
// This is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 3 of the License, or
// (at your option) any later version.
//
// This software is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, see <http://www.gnu.org/licenses/>.
//###########################################################################
#ifndef __SOFTOPID_H
#define __SOFTOPID_H


#include "SizeUtils.h"

#include "TaskMgr.h"

#include "BackgroundSubstraction.h"
#include "RoiCounter.h"


namespace lima
{
  class SoftOpBaseClass
  {
    friend class SoftOpExternalMgr;
  protected:
    static const int DEFAULT_HISTORY_SIZE = 128;

    virtual ~SoftOpBaseClass() {};

    virtual void addTo(TaskMgr&,int stage) = 0;
    virtual void prepare() = 0;
  };

  enum SoftOpId
    {
      UNDEF,
      BACKGROUNDSUBSTRACTION,
      BINNING,
      BPM,
      FLATFIELDCORRECTION,
      FLIP,
      MASK,
      ROICOUNTERS,
      SOFTROI
    };

  struct SoftOpKey
  {
    SoftOpKey() : m_id(UNDEF),m_name(NULL) {};
    SoftOpKey(SoftOpId id,const char *name) : m_id(id),m_name(name) {}

    SoftOpId	m_id;
    const char *m_name;
  };

  struct SoftOpInstance
  {
    SoftOpInstance() : m_linkable(false),
		       m_opt(NULL) {};

    SoftOpInstance(const SoftOpKey &akey,
		   const std::string &anAlias) :
      m_key(akey),
      m_alias(anAlias),m_linkable(false),m_opt(NULL) {}
    SoftOpKey		m_key;
    std::string		m_alias;
    bool		m_linkable;
    SoftOpBaseClass*	m_opt;
  };
  
  class SoftOpBackgroundSubstraction : public SoftOpBaseClass
  {
  public:
    SoftOpBackgroundSubstraction();
    ~SoftOpBackgroundSubstraction();
    
    void setBackgroundImage(Data &aData);
    
  protected:
    virtual void addTo(TaskMgr&,int stage);
    virtual void prepare() {};
  private:
    Tasks::BackgroundSubstraction *m_opt;
  };

  class SoftOpRoiCounter : public SoftOpBaseClass
  {
  public:
    typedef std::pair<int,std::list<Tasks::RoiCounterResult> > RoiIdAndResults;
    typedef std::pair<int,Roi> RoiIdAndRoi;
    SoftOpRoiCounter();
    ~SoftOpRoiCounter();

    void add(const std::list<Roi> &rois); 
    void set(const std::list<Roi> &rois); 
    void get(std::list<Roi>&) const;
    void del(const std::list<int> &roiIds);
    void clearAllRoi();		/* clear all roi */

    void clearCounterStatus();
    int  getCounterStatus() const;

    void setMask(Data &aMask);

    void setBufferSize(int size);
    void getBufferSize(int &size) const;
    
    void readCounters(int from,std::list<RoiIdAndResults> &result) const;
  protected:
    virtual void addTo(TaskMgr&,int stage);
    virtual void prepare();
  private:
    typedef std::pair<Tasks::RoiCounterManager*,Tasks::RoiCounterTask*> ManagerNCounter;

    std::list<ManagerNCounter>  m_manager_tasks;
    int				m_history_size;
    int				m_counter_status;
    Data			m_mask;
    mutable Cond		m_cond;
  };

}
#endif
