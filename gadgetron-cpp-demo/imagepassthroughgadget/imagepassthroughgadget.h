#ifndef IMAGE_PASSTHROUGH_GADGET_H
#define IMAGE_PASSTHROUGH_GADGET_H

#include "Gadget.h"
#include "hoNDArray.h"

#include <ismrmrd/ismrmrd.h>

using namespace Gadgetron;
namespace Gadgetron4Fun{

    class ImagePassthroughGadget:
    public Gadget2<ISMRMRD::ImageHeader,hoNDArray< float > >
{
    public:
    GADGET_DECLARE(ImagePassthroughGadget);

    ImagePassthroughGadget();
    virtual ~ImagePassthroughGadget();

    protected:

    virtual int process(GadgetContainerMessage<ISMRMRD::ImageHeader>* m1,
                        GadgetContainerMessage< hoNDArray< float > >* m2);
    virtual int process_config(ACE_Message_Block *mb);
};
}

#endif //IMAGE_PASSTHROUGH_GADGET_H
